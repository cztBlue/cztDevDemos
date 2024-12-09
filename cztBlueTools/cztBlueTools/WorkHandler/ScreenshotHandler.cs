using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace cztBlueTools.WorkHandler
{
    internal class ScreenshotHandler
    {
        private Rectangle captureRectangle;
        private TextBox pointBox;

        public ScreenshotHandler(TextBox box)
        {
            //captureRectangle = r;
            pointBox = box;
        }

        public void ShotDefault()
        {
            using (Bitmap bitmap = new Bitmap(captureRectangle.Width, captureRectangle.Height))
            {
                // 创建一个Graphics对象，从Bitmap对象中创建
                using (Graphics graphics = Graphics.FromImage(bitmap))
                {
                    // 截取屏幕的指定区域。当使用CopyFromScreen方法时，
                    // 第一个参数指定要开始拷贝的起点（屏幕坐标），
                    // 第二个参数指定Bitmap对象的哪个点为起始点，
                    // 第三个参数指定要拷贝的区域大小
                    graphics.CopyFromScreen(captureRectangle.Location, Point.Empty, captureRectangle.Size);
                }

                // 将截图复制到剪贴板
                Clipboard.SetImage(bitmap);
                Console.WriteLine("Screenshot copied to clipboard.");
            }
        }

        /// <summary>
        /// 传参截图
        /// </summary>
        /// <param name="r"></param>
        public void ShotAren(Rectangle r)
        {
            using (Bitmap bitmap = new Bitmap(r.Width, r.Height))
            {

                using (Graphics graphics = Graphics.FromImage(bitmap))
                {
                    graphics.CopyFromScreen(r.Location, Point.Empty, r.Size);
                }

                // 将截图复制到剪贴板
                Clipboard.SetImage(bitmap);
                Console.WriteLine("Screenshot copied to clipboard.");
            }
        }

        public void Shot()
        {
            var arr = ParseInputHandler.ParsePointInt(pointBox.Text);
            var r = new Rectangle(arr[0], arr[1], arr[2], arr[3]);
            using (Bitmap bitmap = new Bitmap(r.Width, r.Height))
            {

                using (Graphics graphics = Graphics.FromImage(bitmap))
                {
                    graphics.CopyFromScreen(r.Location, Point.Empty, r.Size);
                }

                // 将截图复制到剪贴板
                Clipboard.SetImage(bitmap);
                Console.WriteLine("Screenshot copied to clipboard.");
            }
        }
    }
}
