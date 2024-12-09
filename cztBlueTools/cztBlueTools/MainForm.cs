using cztBlueTools.DataStruct;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;


namespace cztBlueTools
{
    public partial class MainForm : Form
    {
        private List<Panel> allPanelList = new List<Panel> { };
        private Panel panelAutoScreenShot;
        private Panel panelPasswordManager;
        public MainForm()
        {
            InitializeComponent();
            InitPanel();
        }

        public void InitPanel()
        {
            //自动截图Panel初始化
            panelAutoScreenShot = new PanelAutoScreenshot();
            Controls.Add(panelAutoScreenShot);
            allPanelList.Add(panelAutoScreenShot);

            //密码管理Panel初始化
            panelPasswordManager = new PanelPasswordManager();
            Controls.Add(panelPasswordManager);
            allPanelList.Add(panelPasswordManager);
        }

        private void ShowPanel(Panel panelToShow)
        {
            // 隐藏所有面板
            foreach (var item in allPanelList)
            {
                item.Visible = false;
            }

            // 显示目标面板
            panelToShow.Visible = true;
        }

        private void ScreenshotToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ShowPanel(panelAutoScreenShot);
        }

        private void PasswordManagerToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ShowPanel(panelPasswordManager);
            // 类型安全检查+转换
            if (panelPasswordManager is PanelPasswordManager passwordManager)  
            {
                passwordManager.SwitchPanelHandler();  
            }

        }
    }
}
