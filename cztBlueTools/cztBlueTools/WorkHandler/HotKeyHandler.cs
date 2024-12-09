using System;
using System.Collections.Generic;
using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public delegate void OnOKeyPressed();

namespace cztBlueTools
{
    internal class HotKeyHandler : Form
    {
        // 定义 Windows API 函数
        [DllImport("user32.dll")]
        private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);

        [DllImport("user32.dll")]
        private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

        Dictionary<string, Keys> keyMapping = new Dictionary<string, Keys>
            {
                { "Backspace", Keys.Back },
                { "Tab", Keys.Tab },
                { "Enter", Keys.Enter },
                { "Shift", Keys.ShiftKey },
                { "Control", Keys.ControlKey },
                { "Alt", Keys.Menu },
                { "Pause", Keys.Pause },
                { "CapsLock", Keys.CapsLock },
                { "Escape", Keys.Escape },
                { "Space", Keys.Space },
                { "PageUp", Keys.PageUp },
                { "PageDown", Keys.PageDown },
                { "End", Keys.End },
                { "Home", Keys.Home },
                { "LeftArrow", Keys.Left },
                { "UpArrow", Keys.Up },
                { "RightArrow", Keys.Right },
                { "DownArrow", Keys.Down },
                { "Insert", Keys.Insert },
                { "Delete", Keys.Delete },
                { "0", Keys.D0 },
                { "1", Keys.D1 },
                { "2", Keys.D2 },
                { "3", Keys.D3 },
                { "4", Keys.D4 },
                { "5", Keys.D5 },
                { "6", Keys.D6 },
                { "7", Keys.D7 },
                { "8", Keys.D8 },
                { "9", Keys.D9 },
                { "A", Keys.A },
                { "B", Keys.B },
                { "C", Keys.C },
                { "D", Keys.D },
                { "E", Keys.E },
                { "F", Keys.F },
                { "G", Keys.G },
                { "H", Keys.H },
                { "I", Keys.I },
                { "J", Keys.J },
                { "K", Keys.K },
                { "L", Keys.L },
                { "M", Keys.M },
                { "N", Keys.N },
                { "O", Keys.O },
                { "P", Keys.P },
                { "Q", Keys.Q },
                { "R", Keys.R },
                { "S", Keys.S },
                { "T", Keys.T },
                { "U", Keys.U },
                { "V", Keys.V },
                { "W", Keys.W },
                { "X", Keys.X },
                { "Y", Keys.Y },
                { "Z", Keys.Z },
            };

        // 热键定义
        private const int HOTKEY_ID = 9000; // 任何唯一的 ID
        private const uint MOD_NONE = 0x0000; // 无修饰键
        private uint VK = 0x4F; // "O" 键的虚拟键码
        private TextBox HotKeyBindingTextBox { get; set; }
        private OnOKeyPressed keyDownHandler { get; set; }
        private Label stateLabel { get; set; }

        public HotKeyHandler(TextBox Hotkeyinfo, Label stateLabel, OnOKeyPressed keyDownHandler)
        {
            this.keyDownHandler = keyDownHandler;
            HotKeyBindingTextBox = Hotkeyinfo;
            this.stateLabel = stateLabel;
        }

        public void RegisterHotKey_()
        {
            Dispose(false);
            VK = (uint)keyMapping[HotKeyBindingTextBox.Text];
            if (!RegisterHotKey(this.Handle, HOTKEY_ID, MOD_NONE, VK))
            {
                MessageBox.Show("无法注册热键!");
            }
            stateLabel.Text = "状态2：当前热键 "+ HotKeyBindingTextBox.Text;
        }

        public void SetHandler(OnOKeyPressed keyDownHandler)
        {
            this.keyDownHandler = keyDownHandler;
        }

        // 窗口消息处理
        protected override void WndProc(ref Message m)
        {
            base.WndProc(ref m);

            const int WM_HOTKEY = 0x0312;
            // 检查是否为热键消息
            if (m.Msg == WM_HOTKEY && m.WParam.ToInt32() == HOTKEY_ID)
            {
                // 调用所需的函数
                keyDownHandler();
            }
        }

        protected override void Dispose(bool disposing)
        {
            // 注销热键
            try
            {
                UnregisterHotKey(this.Handle, HOTKEY_ID);
                base.Dispose(disposing);
                stateLabel.Text = "状态2：未置热键";
            }
            catch { }

        }

    }
}
