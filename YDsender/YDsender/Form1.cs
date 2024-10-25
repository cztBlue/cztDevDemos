using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Security;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Windows.Forms;

namespace YDsender
{
    public partial class Form1 : Form
    {
        public static string YDCookie = "";
        public static string SK = "";
        public static string STime = "";
        public static string Sign = "";

        public Form1()
        {
            InitializeComponent();
        }



        /// <summary>
        /// 小写32位MD加密
        /// </summary>
        /// <param name="str"></param>
        /// <returns></returns>
        public static string GetMD5_32(string str)
        {
            MD5CryptoServiceProvider md5Hasher = new MD5CryptoServiceProvider();
            byte[] data = md5Hasher.ComputeHash(UTF8Encoding.Default.GetBytes(str));
            StringBuilder sBuilder = new StringBuilder();
            for (int i = 0; i < data.Length; i++)
            {
                sBuilder.Append(data[i].ToString("x2"));//转化为小写的16进制
            }
            return sBuilder.ToString();
        }

        private static long ConvertDateTimeToInt(System.DateTime time)
        {
            System.DateTime startTime = TimeZone.CurrentTimeZone.ToLocalTime(new System.DateTime(1970, 1, 1, 0, 0, 0, 0));
            long t = (time.Ticks - startTime.Ticks) / 10000;   //除10000调整为13位      
            return t;
        }

        /// <summary>
        /// 当前时间13位时间戳
        /// </summary>
        /// <param name="time"></param>
        /// <returns></returns>
        public static string GetTimeStamp()
        {
            System.DateTime time = System.DateTime.Now;
            long ts = ConvertDateTimeToInt(time);
            return ts.ToString();
        }

        /// <summary>
        /// Base64去URL符号解码
        /// </summary>
        /// <param name="urlSafeBase64"></param>
        /// <returns></returns>
        public static byte[] UrlSafeBase64Decode(string urlSafeBase64)
        {
            string base64 = urlSafeBase64.Replace('-', '+').Replace('_', '/');
            int mod4 = base64.Length % 4;
            if (mod4 > 0)
            {
                base64 = base64.PadRight(base64.Length + (4 - mod4), '=');
            }
            return Convert.FromBase64String(base64);
        }

        public static string GetSign(string key, string t)
        {
            return GetMD5_32("client=fanyideskweb&mysticTime=" + t + "&product=webfanyi&key=" + key);
        }
        public static JObject Decrypt(string enstr)
        {
            // 密钥和初始化向量（IV）
            byte[] key = Encoding.UTF8.GetBytes("ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl");
            byte[] iv = Encoding.UTF8.GetBytes("ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4");

            // 创建 AES 解密器
            using (var md5 = MD5.Create())
            {
                byte[] keyHash = md5.ComputeHash(key);
                byte[] ivHash = md5.ComputeHash(iv);

                using (var aes = Aes.Create())
                {
                    aes.Mode = CipherMode.CBC;
                    aes.Key = keyHash.Take(16).ToArray(); // 只使用前 16 字节
                    aes.IV = ivHash.Take(16).ToArray(); // 只使用前 16 字节

                    // 解密 Base64 编码的字符串
                    byte[] cipherBytes = UrlSafeBase64Decode(enstr);
                    using (var decryptor = aes.CreateDecryptor())
                    using (var ms = new MemoryStream(cipherBytes))
                    using (var cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Read))
                    using (var sr = new StreamReader(cs, Encoding.UTF8))
                    {
                        string decryptedString = sr.ReadToEnd();
                        // 解析 JSON
                        return JObject.Parse(decryptedString);
                    }
                }
            }
        }

        /// <summary>
        /// 初始化建立Session获取SK
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Form1_Load(object sender, EventArgs e)
        {
            STime = GetTimeStamp();
            string Sign = GetSign("asdjnjfenknafdfsdfsd", STime);
            string url = "https://dict.youdao.com/webtranslate/key?keyid=webfanyi-key-getter&sign="
             + Sign + "&client=fanyideskweb&product=webfanyi&appVersion=1.0.0&vendor=web&pointParam=client%2CmysticTime%2Cproduct&mysticTime="
             + STime + "&keyfrom=fanyi.web";

            HttpWebRequest request = WebRequest.Create(url) as HttpWebRequest;
            if (url.StartsWith("https", StringComparison.OrdinalIgnoreCase))
            {
                ServicePointManager.ServerCertificateValidationCallback = (object s, X509Certificate certificate, X509Chain chain, SslPolicyErrors errors) => true;
                request.ProtocolVersion = HttpVersion.Version11;
                // 这里设置了协议类型。
                ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072;// SecurityProtocolType.Tls1.2; 
                request.KeepAlive = true;
                ServicePointManager.CheckCertificateRevocationList = true;
                ServicePointManager.DefaultConnectionLimit = 100;
                ServicePointManager.Expect100Continue = false;
            }
            Random rd = new Random();
            int i = rd.Next(100000000, 999999999);
            YDCookie = "OUTFOX_SEARCH_USER_ID=" + rd.Next(100000000, 999999999) + "@" + rd.Next(1, 255) + "." + rd.Next(1, 255) + "." + rd.Next(1, 255) + "." + rd.Next(1, 255) +
                "; OUTFOX_SEARCH_USER_ID_NCOO=" + rd.Next(100000000, 999999999) + "." + rd.Next(100000000, 999999999);
            request.Method = "GET";
            request.Headers.Add("Accept-Encoding", "identity");
            request.UserAgent = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36";
            request.Referer = "https://fanyi.youdao.com/";
            request.Headers.Add("Cookie", YDCookie);
            request.Headers.Add("origin", "https://fanyi.youdao.com");

            //获取网页响应结果
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            Stream stream = response.GetResponseStream();
            string result = string.Empty;
            using (StreamReader sr = new StreamReader(stream))
            {
                result = sr.ReadToEnd();
            }

            JObject json = JObject.Parse(result);
            SK = json["data"]["secretKey"].ToString();
        }
        private void btnstart_Click(object sender, EventArgs e)
        {
            if (SK != "")
            {
                MessageBox.Show("当前Session:" + SK);
            }
            else
            {
                MessageBox.Show("当前Session:" + SK);
            }
        }

        /// <summary>
        /// 发送文本，获取翻译
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void work_Click(object sender, EventArgs e)
        {
            string url = "https://dict.youdao.com/webtranslate";
            HttpWebRequest request = WebRequest.Create(url) as HttpWebRequest;
            if (url.StartsWith("https", StringComparison.OrdinalIgnoreCase))
            {
                ServicePointManager.ServerCertificateValidationCallback = (object s, X509Certificate certificate, X509Chain chain, SslPolicyErrors errors) => true;
                request.ProtocolVersion = HttpVersion.Version11;
                // 这里设置了协议类型。
                ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072;// SecurityProtocolType.Tls1.2; 
                request.KeepAlive = false;
                ServicePointManager.CheckCertificateRevocationList = true;
                ServicePointManager.DefaultConnectionLimit = 100;
                ServicePointManager.Expect100Continue = false;
            }
            request.Method = "POST";
            request.Headers.Add("Accept-Encoding", "identity");
            request.UserAgent = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36";
            request.Referer = "https://fanyi.youdao.com/";
            request.Headers.Add("Cookie", YDCookie);
            request.Headers.Add("origin", "https://fanyi.youdao.com");
            request.ContentType = "application/x-www-form-urlencoded";
            string curtime = GetTimeStamp();

            try
            {
                if (textBoxRaw.Text == "" || textBoxRaw.Text is null)
                {
                    MessageBox.Show("输入文本后再试");
                    return;
                }
                string postData = "i=" + textBoxRaw.Text +
                "&from=auto&to=auto&dictResult=True&keyid=webfanyi&sign=" + GetSign(SK, curtime) +
                "&client=fanyideskweb&product=webfanyi&appVersion=1.0.0&vendor=web&pointParam=client%2CmysticTime%2Cproduct&" +
                "mysticTime=" + curtime +
                "&keyfrom=fanyi.web";
                byte[] data = Encoding.UTF8.GetBytes(postData);
                request.ContentLength = data.Length;
                Stream newStream = request.GetRequestStream();
                newStream.Write(data, 0, data.Length);
                newStream.Close();
                //获取网页响应结果
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                Stream stream = response.GetResponseStream();
                string result = string.Empty;
                using (StreamReader sr = new StreamReader(stream))
                {
                    result = sr.ReadToEnd();
                }
                JObject res = Decrypt(result);
                textBoxRes.Text = ((JObject)res["translateResult"][0][0])["tgt"].ToString();
            }
            catch
            {
                MessageBox.Show("SK异常，请刷新Session");
            }

        }
    }
}
