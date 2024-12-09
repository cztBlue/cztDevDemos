using System;
using System.Runtime.InteropServices;
using System.Threading;
using WindowsInput;
using WindowsInput.Native;
using System.Windows.Forms;  // 引入 Windows Forms 命名空间

namespace cztBlueTools.WorkHandler
{
    internal class ClickMockHandler
    {
        private TextBox inputTextBox { get; set; }

        public ClickMockHandler(TextBox inputTextBox)
        {
            this.inputTextBox = inputTextBox;
        }


        public void MouseClick()
        {
            //int posx, int posy, string focus = ""
            var arr = ParseInputHandler.ParsePointInt(inputTextBox.Text);
            var sim = new InputSimulator();

            // 执行移动和左键点击
            SmoothMoveAndLeftClick(sim, arr[0], arr[1]);

        }

        static void MoveAndLeftClick(InputSimulator sim, int x, int y)
        {
            int screenWidth = Screen.PrimaryScreen.Bounds.Width;
            int screenHeight = Screen.PrimaryScreen.Bounds.Height;

            // 将屏幕坐标转换为虚拟桌面范围
            double virtualX = (x / (double)screenWidth) * 65535;
            double virtualY = (y / (double)screenHeight) * 65535;

            // 移动鼠标并左键点击
            sim.Mouse.MoveMouseTo(virtualX, virtualY)
                     .LeftButtonClick();
        }

        static void SmoothMoveAndLeftClick(InputSimulator sim, int targetX, int targetY)
        {
            int currentX = Cursor.Position.X;
            int currentY = Cursor.Position.Y;

            // 步进调节量和延迟设置
            int stepCount = 100;
            int delayMilliseconds = 5;

            for (int step = 0; step < stepCount; step++)
            {
                // 计算当前位置到目标位置的插值点
                double t = (double)step / stepCount;
                int intermediateX = (int)(currentX + t * (targetX - currentX));
                int intermediateY = (int)(currentY + t * (targetY - currentY));

                // 将屏幕坐标转换为虚拟桌面范围
                double virtualX = (intermediateX / (double)Screen.PrimaryScreen.Bounds.Width) * 65535;
                double virtualY = (intermediateY / (double)Screen.PrimaryScreen.Bounds.Height) * 65535;

                // 移动到中间位置
                sim.Mouse.MoveMouseTo(virtualX, virtualY);

                // 延迟
                Thread.Sleep(delayMilliseconds);
            }

            // 最后一次确保在目标位置
            MoveAndLeftClick(sim, targetX, targetY);
        }

        [DllImport("user32.dll", SetLastError = true)]
        private static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool SetForegroundWindow(IntPtr hWnd);

        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        private const int SW_RESTORE = 9;

        public void SetFoucs(string title)
        {
            // 使用窗口标题寻找窗口句柄（你需要用目标应用程序的标题替换下面的 "Untitled - Notepad"）
            IntPtr hWnd = FindWindow(null, title);

            if (hWnd != IntPtr.Zero)
            {
                // 使窗口在前台
                SetForegroundWindow(hWnd);

                // 如果窗口最小化，将其恢复
                ShowWindow(hWnd, SW_RESTORE);

                // 给窗口一些时间来处理过渡
                Thread.Sleep(200);

                // 在此处添加你的鼠标点击代码
                // MouseClick(500, 300);
                Console.WriteLine("Window is brought to the foreground.");
            }
            else
            {
                Console.WriteLine("Window not found.");
            }
        }
    }
}
