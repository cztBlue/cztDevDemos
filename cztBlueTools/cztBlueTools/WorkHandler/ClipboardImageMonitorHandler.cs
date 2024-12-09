using System;
using System.Drawing;
using System.IO;
using System.Security.Cryptography;
using System.Windows.Forms;

namespace cztBlueTools.WorkHandler
{
    internal class ClipboardImageMonitorHandler
    {
        private System.Windows.Forms.Timer clipboardTimer { get; set; }
        private string lastPngHash { get; set; }
        private TextBox boxCount { get; set; }
        private TextBox boxPath { get; set; }
        private Label showState { get; set; }
        private bool isOnMoniter
        {
            set
            {
                if (value == false)
                {
                    showState.Text = "状态1:停止监听剪贴板";
                }

                if (value == true)
                {
                    showState.Text = "状态1:正在监听剪贴板";
                }
            }
        }

        public ClipboardImageMonitorHandler(TextBox boxPath_, TextBox boxCount_, Label state)
        {
            clipboardTimer = new System.Windows.Forms.Timer();
            clipboardTimer.Interval = 100; // 每100毫秒检查一次
            clipboardTimer.Tick += ClipboardTimer_Tick;
 
            boxPath = boxPath_;
            boxCount = boxCount_;
            showState = state;

            isOnMoniter = false;
        }

        public void StartMonitor()
        {
            clipboardTimer.Start();
            isOnMoniter = true;
        }

        public void StopMonitor()
        {
            clipboardTimer.Stop();
            isOnMoniter = false;
        }

        private void ClipboardTimer_Tick(object sender, EventArgs e)
        {
            try
            {
                if (Clipboard.ContainsImage())
                {
                    Image clipboardImage = Clipboard.GetImage();
                    using (MemoryStream ms = new MemoryStream())
                    {
                        clipboardImage.Save(ms, System.Drawing.Imaging.ImageFormat.Png);
                        byte[] imageBytes = ms.ToArray();

                        string currentPngHash = GetImageHash(imageBytes);
                        if (currentPngHash != lastPngHash)
                        {
                            int? b = int.Parse(boxCount.Text);
                            int count = b ?? 1;
                            var path = boxPath.Text ?? "D://codeD";
                            ValidPath(path);
                            string filePath = Path.Combine(path, $"{count}.png");
                            File.WriteAllBytes(filePath, imageBytes);

                            Console.WriteLine($"Saved new PNG image as {filePath}");
                            lastPngHash = currentPngHash;
                            count++;
                            boxCount.Text = count.ToString();
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        private string GetImageHash(byte[] imageBytes)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] hashBytes = sha256.ComputeHash(imageBytes);
                return Convert.ToBase64String(hashBytes);
            }
        }

        public static bool IsValidPath(string path)
        {
            try
            {
                // 尝试创建一个 FileInfo 或 DirectoryInfo 对象，仅用于验证路径格式
                var info = new FileInfo(path);
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }
        public static void ValidPath(string path)
        {

            if (!Directory.Exists(path))
            {
                // 如果不存在，则创建目录
                Directory.CreateDirectory(path);
                Console.WriteLine($"Directory created: {path}");
            }
            else
            {
                Console.WriteLine($"Directory already exists: {path}");
            }
        }

    }
}
