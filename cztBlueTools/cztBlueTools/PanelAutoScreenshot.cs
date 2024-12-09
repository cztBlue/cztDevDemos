using cztBlueTools.WorkHandler;
using System.Drawing;
using System.Windows.Forms;


namespace cztBlueTools
{
    internal class PanelAutoScreenshot : Panel
    {
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.SaveNameIterTextBox = new System.Windows.Forms.TextBox();
            this.SavePathTextBox = new System.Windows.Forms.TextBox();
            this.StartMonitorClipButton = new System.Windows.Forms.Button();
            this.ScreenshotRectanglePointTextBox = new System.Windows.Forms.TextBox();
            this.ScreenshotButton = new System.Windows.Forms.Button();
            this.StopMonitorClipButton = new System.Windows.Forms.Button();
            this.IsOnClipMoniterLabel = new System.Windows.Forms.Label();
            this.HotKeyScreenshotTextBox = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.InjectHotKeyButton = new System.Windows.Forms.Button();
            this.IsOnHotKeyLabel = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.label8 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.ClickPointTextBox = new System.Windows.Forms.TextBox();
            this.FocusWindowTextBox = new System.Windows.Forms.TextBox();
            this.ClickScreenshotDelayTextBox = new System.Windows.Forms.TextBox();
            this.ActionCountTextBox = new System.Windows.Forms.TextBox();
            this.MouseClickButton = new System.Windows.Forms.Button();
            this.InjectFocusButton = new System.Windows.Forms.Button();
            this.StartActionButton = new System.Windows.Forms.Button();
            this.StopActionButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(0, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(100, 23);
            this.label1.TabIndex = 0;
            this.label1.Text = "下次保存名称";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(100, 23);
            this.label2.TabIndex = 0;
            this.label2.Text = "保存路径";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(0, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(100, 23);
            this.label3.TabIndex = 0;
            this.label3.Text = "截图坐标";
            // 
            // SaveNameIterTextBox
            // 
            this.SaveNameIterTextBox.Location = new System.Drawing.Point(0, 0);
            this.SaveNameIterTextBox.Name = "SaveNameIterTextBox";
            this.SaveNameIterTextBox.Size = new System.Drawing.Size(100, 25);
            this.SaveNameIterTextBox.TabIndex = 0;
            this.SaveNameIterTextBox.Text = "1";
            // 
            // SavePathTextBox
            // 
            this.SavePathTextBox.Location = new System.Drawing.Point(0, 0);
            this.SavePathTextBox.Name = "SavePathTextBox";
            this.SavePathTextBox.Size = new System.Drawing.Size(100, 25);
            this.SavePathTextBox.TabIndex = 0;
            this.SavePathTextBox.Text = "D:\\\\codeD\\\\Temp";
            // 
            // StartMonitorClipButton
            // 
            this.StartMonitorClipButton.Location = new System.Drawing.Point(0, 0);
            this.StartMonitorClipButton.Name = "StartMonitorClipButton";
            this.StartMonitorClipButton.Size = new System.Drawing.Size(75, 23);
            this.StartMonitorClipButton.TabIndex = 0;
            this.StartMonitorClipButton.Text = "开始监听";
            this.StartMonitorClipButton.UseVisualStyleBackColor = true;
            this.StartMonitorClipButton.Click += new System.EventHandler(this.StartMonitorClipButton_Click);
            // 
            // ScreenshotRectanglePointTextBox
            // 
            this.ScreenshotRectanglePointTextBox.Location = new System.Drawing.Point(0, 0);
            this.ScreenshotRectanglePointTextBox.Name = "ScreenshotRectanglePointTextBox";
            this.ScreenshotRectanglePointTextBox.Size = new System.Drawing.Size(100, 25);
            this.ScreenshotRectanglePointTextBox.TabIndex = 0;
            this.ScreenshotRectanglePointTextBox.Text = "(0,0,100,100)";
            // 
            // ScreenshotButton
            // 
            this.ScreenshotButton.Location = new System.Drawing.Point(0, 0);
            this.ScreenshotButton.Name = "ScreenshotButton";
            this.ScreenshotButton.Size = new System.Drawing.Size(75, 23);
            this.ScreenshotButton.TabIndex = 0;
            this.ScreenshotButton.Text = "截图";
            this.ScreenshotButton.UseVisualStyleBackColor = true;
            this.ScreenshotButton.Click += new System.EventHandler(this.ScreenshotButton_Click);
            // 
            // StopMonitorClipButton
            // 
            this.StopMonitorClipButton.Location = new System.Drawing.Point(0, 0);
            this.StopMonitorClipButton.Name = "StopMonitorClipButton";
            this.StopMonitorClipButton.Size = new System.Drawing.Size(75, 23);
            this.StopMonitorClipButton.TabIndex = 0;
            this.StopMonitorClipButton.Text = "停止监听";
            this.StopMonitorClipButton.UseVisualStyleBackColor = true;
            this.StopMonitorClipButton.Click += new System.EventHandler(this.StopMonitorClipButton_Click);
            // 
            // IsOnClipMoniterLabel
            // 
            this.IsOnClipMoniterLabel.AutoSize = true;
            this.IsOnClipMoniterLabel.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.IsOnClipMoniterLabel.Location = new System.Drawing.Point(0, 0);
            this.IsOnClipMoniterLabel.Name = "IsOnClipMoniterLabel";
            this.IsOnClipMoniterLabel.Size = new System.Drawing.Size(100, 23);
            this.IsOnClipMoniterLabel.TabIndex = 0;
            this.IsOnClipMoniterLabel.Text = "保存路径";
            // 
            // HotKeyScreenshotTextBox
            // 
            this.HotKeyScreenshotTextBox.Location = new System.Drawing.Point(0, 0);
            this.HotKeyScreenshotTextBox.Name = "HotKeyScreenshotTextBox";
            this.HotKeyScreenshotTextBox.Size = new System.Drawing.Size(100, 25);
            this.HotKeyScreenshotTextBox.TabIndex = 0;
            this.HotKeyScreenshotTextBox.Text = "S";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(0, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(100, 23);
            this.label4.TabIndex = 0;
            this.label4.Text = "截图热键";
            // 
            // InjectHotKeyButton
            // 
            this.InjectHotKeyButton.Location = new System.Drawing.Point(0, 0);
            this.InjectHotKeyButton.Name = "InjectHotKeyButton";
            this.InjectHotKeyButton.Size = new System.Drawing.Size(75, 23);
            this.InjectHotKeyButton.TabIndex = 0;
            this.InjectHotKeyButton.Text = "注入热键";
            this.InjectHotKeyButton.UseVisualStyleBackColor = true;
            this.InjectHotKeyButton.Click += new System.EventHandler(this.InjectHotKeyButton_Click);
            // 
            // IsOnHotKeyLabel
            // 
            this.IsOnHotKeyLabel.AutoSize = true;
            this.IsOnHotKeyLabel.Location = new System.Drawing.Point(0, 0);
            this.IsOnHotKeyLabel.Name = "IsOnHotKeyLabel";
            this.IsOnHotKeyLabel.Size = new System.Drawing.Size(100, 23);
            this.IsOnHotKeyLabel.TabIndex = 0;
            this.IsOnHotKeyLabel.Text = "状态2：未置热键";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(0, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(100, 23);
            this.label5.TabIndex = 0;
            this.label5.Text = "Unsafe\\dev Func:";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(0, 0);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(100, 23);
            this.label6.TabIndex = 0;
            this.label6.Text = "点击坐标";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(0, 0);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(100, 23);
            this.label7.TabIndex = 0;
            this.label7.Text = "焦点窗口";
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(0, 0);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(100, 23);
            this.label8.TabIndex = 0;
            this.label8.Text = "Delay/s";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(0, 0);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(100, 23);
            this.label9.TabIndex = 0;
            this.label9.Text = "动作次数";
            // 
            // ClickPointTextBox
            // 
            this.ClickPointTextBox.Location = new System.Drawing.Point(0, 0);
            this.ClickPointTextBox.Name = "ClickPointTextBox";
            this.ClickPointTextBox.Size = new System.Drawing.Size(100, 25);
            this.ClickPointTextBox.TabIndex = 0;
            this.ClickPointTextBox.Text = "(100,100)";
            // 
            // FocusWindowTextBox
            // 
            this.FocusWindowTextBox.Location = new System.Drawing.Point(0, 0);
            this.FocusWindowTextBox.Name = "FocusWindowTextBox";
            this.FocusWindowTextBox.Size = new System.Drawing.Size(100, 25);
            this.FocusWindowTextBox.TabIndex = 0;
            // 
            // ClickScreenshotDelayTextBox
            // 
            this.ClickScreenshotDelayTextBox.Location = new System.Drawing.Point(0, 0);
            this.ClickScreenshotDelayTextBox.Name = "ClickScreenshotDelayTextBox";
            this.ClickScreenshotDelayTextBox.Size = new System.Drawing.Size(100, 25);
            this.ClickScreenshotDelayTextBox.TabIndex = 0;
            this.ClickScreenshotDelayTextBox.Text = "(1,0.3)";
            // 
            // ActionCountTextBox
            // 
            this.ActionCountTextBox.Location = new System.Drawing.Point(0, 0);
            this.ActionCountTextBox.Name = "ActionCountTextBox";
            this.ActionCountTextBox.Size = new System.Drawing.Size(100, 25);
            this.ActionCountTextBox.TabIndex = 0;
            this.ActionCountTextBox.Text = "0";
            // 
            // MouseClickButton
            // 
            this.MouseClickButton.Location = new System.Drawing.Point(0, 0);
            this.MouseClickButton.Name = "MouseClickButton";
            this.MouseClickButton.Size = new System.Drawing.Size(75, 23);
            this.MouseClickButton.TabIndex = 0;
            this.MouseClickButton.Text = "点击模拟";
            this.MouseClickButton.UseVisualStyleBackColor = true;
            this.MouseClickButton.Click += new System.EventHandler(this.MouseClickButton_Click);
            // 
            // InjectFocusButton
            // 
            this.InjectFocusButton.Location = new System.Drawing.Point(0, 0);
            this.InjectFocusButton.Name = "InjectFocusButton";
            this.InjectFocusButton.Size = new System.Drawing.Size(75, 23);
            this.InjectFocusButton.TabIndex = 0;
            this.InjectFocusButton.Text = "注入焦点";
            this.InjectFocusButton.UseVisualStyleBackColor = true;
            this.InjectFocusButton.Click += new System.EventHandler(this.InjectFocusButton_Click);
            // 
            // StartActionButton
            // 
            this.StartActionButton.Location = new System.Drawing.Point(0, 0);
            this.StartActionButton.Name = "StartActionButton";
            this.StartActionButton.Size = new System.Drawing.Size(75, 23);
            this.StartActionButton.TabIndex = 0;
            this.StartActionButton.Text = "开始动作";
            this.StartActionButton.UseVisualStyleBackColor = true;
            // 
            // StopActionButton
            // 
            this.StopActionButton.Location = new System.Drawing.Point(0, 0);
            this.StopActionButton.Name = "StopActionButton";
            this.StopActionButton.Size = new System.Drawing.Size(75, 23);
            this.StopActionButton.TabIndex = 0;
            this.StopActionButton.Text = "结束动作";
            this.StopActionButton.UseVisualStyleBackColor = true;
            this.ResumeLayout(false);

        }

        private const int verticalSpacing = 35;
        private Label label1;
        private Label label2;
        private Label label3;
        private TextBox SavePathTextBox;
        private Button StartMonitorClipButton;
        private TextBox ScreenshotRectanglePointTextBox;
        private Button ScreenshotButton;
        private Button StopMonitorClipButton;
        private Label IsOnClipMoniterLabel;
        private TextBox HotKeyScreenshotTextBox;
        private Label label4;
        private Button InjectHotKeyButton;
        private Label IsOnHotKeyLabel;
        private Label label5;
        private Label label6;
        private Label label7;
        private Label label8;
        private Label label9;
        private TextBox ClickPointTextBox;
        private TextBox FocusWindowTextBox;
        private TextBox ClickScreenshotDelayTextBox;
        private TextBox ActionCountTextBox;
        private Button MouseClickButton;
        private Button InjectFocusButton;
        private Button StartActionButton;
        private Button StopActionButton;
        private TextBox SaveNameIterTextBox;

        public PanelAutoScreenshot()
        {
            Name = "PanelAutoScreenshot";
            Size = new Size(1000, 500);
            Location = new Point(0, 50);
            Visible = true;

            InitializeComponent();
            AfterInitializeComponent();
        }

        private void AfterInitializeComponent()
        {
            //添加组件附属
            Controls.Add(label1);
            Controls.Add(label2);
            Controls.Add(label3);
            Controls.Add(label4);
            Controls.Add(SavePathTextBox);
            Controls.Add(StartMonitorClipButton);
            Controls.Add(ScreenshotRectanglePointTextBox);
            Controls.Add(ScreenshotButton);
            Controls.Add(StopMonitorClipButton);
            Controls.Add(SaveNameIterTextBox);
            Controls.Add(IsOnClipMoniterLabel);
            Controls.Add(HotKeyScreenshotTextBox);
            Controls.Add(InjectHotKeyButton);
            Controls.Add(IsOnHotKeyLabel);
            Controls.Add(label5);
            Controls.Add(label6);
            Controls.Add(label7);
            Controls.Add(label8);
            Controls.Add(label9);
            Controls.Add(ClickPointTextBox);
            Controls.Add(FocusWindowTextBox);
            Controls.Add(ClickScreenshotDelayTextBox);
            Controls.Add(ActionCountTextBox);
            Controls.Add(MouseClickButton);
            Controls.Add(InjectFocusButton);
            Controls.Add(StartActionButton);
            Controls.Add(StopActionButton);

            //确定组件位置
            label1.Location = new Point(20, verticalSpacing * 0);
            IsOnClipMoniterLabel.Location = new Point(450, verticalSpacing * 0);
            label2.Location = new Point(20, verticalSpacing * 1);
            IsOnHotKeyLabel.Location = new Point(450, verticalSpacing * 1);
            label4.Location = new Point(450, verticalSpacing * 2);
            label3.Location = new Point(20, verticalSpacing * 2);
            label5.Location = new Point(20, verticalSpacing * 3);
            label6.Location = new Point(20, verticalSpacing * 4);
            label7.Location = new Point(20, verticalSpacing * 5);
            label8.Location = new Point(20, verticalSpacing * 6);
            label9.Location = new Point(20, verticalSpacing * 7);

            SaveNameIterTextBox.Location = new Point(130, verticalSpacing * 0);
            SavePathTextBox.Location = new Point(130, verticalSpacing * 1);
            HotKeyScreenshotTextBox.Location = new Point(530, verticalSpacing * 2);
            ScreenshotRectanglePointTextBox.Location = new Point(130, verticalSpacing * 2);
            ClickPointTextBox.Location = new Point(130, verticalSpacing * 4);
            FocusWindowTextBox.Location = new Point(130, verticalSpacing * 5);
            ClickScreenshotDelayTextBox.Location = new Point(130, verticalSpacing * 6);
            ActionCountTextBox.Location = new Point(130, verticalSpacing * 7);

            Controls.Add(ClickPointTextBox);
            Controls.Add(FocusWindowTextBox);
            Controls.Add(ClickScreenshotDelayTextBox);
            Controls.Add(ActionCountTextBox);
            Controls.Add(SaveNameIterTextBox);

            StartMonitorClipButton.Location = new Point(250, verticalSpacing * 0);
            StopMonitorClipButton.Location = new Point(250, verticalSpacing * 1);
            InjectHotKeyButton.Location = new Point(645, verticalSpacing * 2);
            ScreenshotButton.Location = new Point(250, verticalSpacing * 2);
            MouseClickButton.Location = new Point(250, verticalSpacing * 4);
            InjectFocusButton.Location = new Point(250, verticalSpacing * 5);
            StartActionButton.Location = new Point(250, verticalSpacing * 6);
            StopActionButton.Location = new Point(250, verticalSpacing * 7);


            //初始化功能，注入一些Handler
            clipmon = new ClipboardImageMonitorHandler(SavePathTextBox, SaveNameIterTextBox, IsOnClipMoniterLabel);
            screenshothandler = new ScreenshotHandler(ScreenshotRectanglePointTextBox);
            hotKeyhandler = new HotKeyHandler(HotKeyScreenshotTextBox, IsOnHotKeyLabel, () => { screenshothandler.Shot(); });
            clickMockHandler = new ClickMockHandler(ClickPointTextBox);
        }

        

        private ClipboardImageMonitorHandler clipmon = null;
        private ScreenshotHandler screenshothandler = null;
        private ClickMockHandler clickMockHandler = null;
        private ParseInputHandler parseInputHandler = null;
        private System.Windows.Forms.Timer clickScrreenActionTimer = null;
        private HotKeyHandler hotKeyhandler = null;

        private void StartMonitorClipButton_Click(object sender, System.EventArgs e)
        {
            clipmon.StartMonitor();
        }

        private void StopMonitorClipButton_Click(object sender, System.EventArgs e)
        {
            try { clipmon.StopMonitor(); } catch { }
        }

        private void ScreenshotButton_Click(object sender, System.EventArgs e)
        {
            screenshothandler.Shot();
        }

        private void InjectHotKeyButton_Click(object sender, System.EventArgs e)
        {
            hotKeyhandler.RegisterHotKey_();
        }

        private void MouseClickButton_Click(object sender, System.EventArgs e)
        {
            clickMockHandler.MouseClick();
        }

        
        private void InjectFocusButton_Click(object sender, System.EventArgs e)
        {
            clickMockHandler.SetFoucs(FocusWindowTextBox.Text);
        }
    }
}
