using cztBlueTools.DataStruct;
using Svg;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace cztBlueTools
{
    internal class PanelPasswordManager : Panel
    {
        private void InitializeComponent()
        {
            this.AccountlistBox = new System.Windows.Forms.ListBox();
            this.PasswordTextBox = new System.Windows.Forms.TextBox();
            this.AddButton = new System.Windows.Forms.Button();
            this.DeleteButton = new System.Windows.Forms.Button();
            this.FliterTextBox = new System.Windows.Forms.TextBox();
            this.ImportJsonButton = new System.Windows.Forms.Button();
            this.ExportJsonButton = new System.Windows.Forms.Button();
            this.SynSQLliteButton = new System.Windows.Forms.Button();
            this.ExportSQLiteButton = new System.Windows.Forms.Button();
            this.ExportTXTButton = new System.Windows.Forms.Button();
            this.ImportTXTButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // AccountlistBox
            // 
            this.AccountlistBox.FormattingEnabled = true;
            this.AccountlistBox.Location = new System.Drawing.Point(0, 0);
            this.AccountlistBox.Name = "AccountlistBox";
            this.AccountlistBox.Size = new System.Drawing.Size(200, 300);
            this.AccountlistBox.TabIndex = 0;
            this.AccountlistBox.SelectedIndexChanged += new System.EventHandler(this.AccountlistBox_SelectedIndexChanged);
            // 
            // PasswordTextBox
            // 
            this.PasswordTextBox.Location = new System.Drawing.Point(0, 0);
            this.PasswordTextBox.Name = "PasswordTextBox";
            this.PasswordTextBox.Size = new System.Drawing.Size(400, 25);
            this.PasswordTextBox.TabIndex = 0;
            // 
            // AddButton
            // 
            this.AddButton.Location = new System.Drawing.Point(0, 0);
            this.AddButton.Name = "AddButton";
            this.AddButton.Size = new System.Drawing.Size(75, 23);
            this.AddButton.TabIndex = 0;
            this.AddButton.Text = "新增";
            this.AddButton.UseVisualStyleBackColor = true;
            // 
            // DeleteButton
            // 
            this.DeleteButton.Location = new System.Drawing.Point(0, 0);
            this.DeleteButton.Name = "DeleteButton";
            this.DeleteButton.Size = new System.Drawing.Size(75, 23);
            this.DeleteButton.TabIndex = 0;
            this.DeleteButton.Text = "删除";
            this.DeleteButton.UseVisualStyleBackColor = true;
            // 
            // FliterTextBox
            // 
            this.FliterTextBox.Location = new System.Drawing.Point(0, 0);
            this.FliterTextBox.Name = "FliterTextBox";
            this.FliterTextBox.Size = new System.Drawing.Size(100, 25);
            this.FliterTextBox.TabIndex = 0;
            // 
            // ImportJsonButton
            // 
            this.ImportJsonButton.Location = new System.Drawing.Point(0, 0);
            this.ImportJsonButton.Name = "ImportJsonButton";
            this.ImportJsonButton.Size = new System.Drawing.Size(75, 23);
            this.ImportJsonButton.TabIndex = 0;
            this.ImportJsonButton.Text = "从Json导入";
            this.ImportJsonButton.UseVisualStyleBackColor = true;
            // 
            // ExportJsonButton
            // 
            this.ExportJsonButton.Location = new System.Drawing.Point(0, 0);
            this.ExportJsonButton.Name = "ExportJsonButton";
            this.ExportJsonButton.Size = new System.Drawing.Size(75, 23);
            this.ExportJsonButton.TabIndex = 0;
            this.ExportJsonButton.Text = "导出到Json";
            this.ExportJsonButton.UseVisualStyleBackColor = true;
            // 
            // SynSQLliteButton
            // 
            this.SynSQLliteButton.Location = new System.Drawing.Point(0, 0);
            this.SynSQLliteButton.Name = "SynSQLliteButton";
            this.SynSQLliteButton.Size = new System.Drawing.Size(75, 23);
            this.SynSQLliteButton.TabIndex = 0;
            this.SynSQLliteButton.Text = "同步到数据库";
            this.SynSQLliteButton.UseVisualStyleBackColor = true;
            // 
            // ExportSQLiteButton
            // 
            this.ExportSQLiteButton.Location = new System.Drawing.Point(0, 0);
            this.ExportSQLiteButton.Name = "ExportSQLiteButton";
            this.ExportSQLiteButton.Size = new System.Drawing.Size(75, 23);
            this.ExportSQLiteButton.TabIndex = 0;
            this.ExportSQLiteButton.Text = "导出到Json";
            this.ExportSQLiteButton.UseVisualStyleBackColor = true;
            // 
            // ExportTXTButton
            // 
            this.ExportTXTButton.Location = new System.Drawing.Point(0, 0);
            this.ExportTXTButton.Name = "ExportTXTButton";
            this.ExportTXTButton.Size = new System.Drawing.Size(75, 23);
            this.ExportTXTButton.TabIndex = 0;
            this.ExportTXTButton.Text = "生成Txt";
            this.ExportTXTButton.UseVisualStyleBackColor = true;
            // 
            // ImportTXTButton
            // 
            this.ImportTXTButton.Location = new System.Drawing.Point(0, 0);
            this.ImportTXTButton.Name = "ImportTXTButton";
            this.ImportTXTButton.Size = new System.Drawing.Size(75, 23);
            this.ImportTXTButton.TabIndex = 0;
            this.ImportTXTButton.Text = "从TXT导入";
            this.ImportTXTButton.UseVisualStyleBackColor = true;
            this.ResumeLayout(false);

        }

        private ListBox AccountlistBox;
        private TextBox PasswordTextBox;
        private Button AddButton;
        private Button DeleteButton;
        private TextBox FliterTextBox;
        private Button ImportJsonButton;
        private Button ExportJsonButton;
        private Button SynSQLliteButton;
        private Button ExportSQLiteButton;
        private Button ExportTXTButton;
        private Button ImportTXTButton;
        private List<AccountData> accountObjs = new List<AccountData>();

        //TextBox detailTextBox;

        public PanelPasswordManager()
        {
            Name = "PanelPasswordManager";
            Size = new Size(1000, 1000);
            Location = new Point(0, 28);
            Visible = false;

            InitializeComponent();
            AfterInitializeComponent();
        }

        public void SwitchPanelHandler()
        {
            AccountlistBox.SetSelected(0, true);
            AccountlistBox.Focus();
        }

        private void AfterInitializeComponent()
        {
            //添加组件附属
            Controls.Add(AccountlistBox);
            Controls.Add(PasswordTextBox);
            Controls.Add(AddButton);
            Controls.Add(DeleteButton);
            Controls.Add(FliterTextBox);
            Controls.Add(ImportJsonButton);
            Controls.Add(ExportJsonButton);
            Controls.Add(SynSQLliteButton);
            Controls.Add(ExportSQLiteButton);
            Controls.Add(ExportTXTButton);
            Controls.Add(ImportTXTButton);

            //确定组件位置
            AddButton.Location = new Point(130, 10);
            DeleteButton.Location = new Point(210, 10);
            ImportJsonButton.Location = new Point(300, 10);
            ExportJsonButton.Location = new Point(380, 10);
            SynSQLliteButton.Location = new Point(460, 10);
            ExportSQLiteButton.Location = new Point(540, 10);
            ExportTXTButton.Location = new Point(620, 10);
            ImportTXTButton.Location = new Point(700, 10);

            FliterTextBox.Location = new Point(20, 10);
            AccountlistBox.Location = new Point(20, 40);
            PasswordTextBox.Location = new Point(240, 40);

            //...
            setData(); //mock data
            AccountlistBox.DrawMode = DrawMode.OwnerDrawFixed;
            AccountlistBox.DrawItem += AccountlistBox_DrawItem;
            AccountlistBox.ItemHeight = 50;
        }

        public void setData()
        {
            accountObjs.Add(new AccountData("Unity", "2691169154@qq.com", "unityrxt6AD6J"));
            accountObjs.Add(new AccountData("nity", "2691169154@qq.com", "ut6AD6J"));

            // 添加简洁的名称到 ListBox
            foreach (var data in accountObjs)
            {
                AccountlistBox.Items.Add(data.BelongTo);
            }
        }

        // 当选中 ListBox 中的项时，显示详细信息
        private void AccountlistBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            ListBox listBox = sender as ListBox;
            if (listBox.SelectedIndex != -1)
            {
                // 获取选中的数据对象并更新 TextBox
                var selectedData = accountObjs[listBox.SelectedIndex];
                PasswordTextBox.Text = selectedData.Password;
            }
        }


        private void AccountlistBox_DrawItem(object sender, DrawItemEventArgs e)
        {

            ListBox listBox = sender as ListBox;

            if (e.Index < 0)
                return;

            e.DrawBackground();

            // 绘制SVG图标代码
            SvgDocument svgDoc;
            using (var svgStream = System.IO.File.OpenRead("D:\\Temporary\\key-svgrepo-com.svg"))
            {
                svgDoc = SvgDocument.Open<SvgDocument>(svgStream);
            }

            Bitmap bitmap = svgDoc.Draw();  // 可以指定大小，比如 (40, 40)

            // 确定图标位置
            int iconSize = 40;
            int iconX = e.Bounds.Left + 5;
            int iconY = e.Bounds.Top + (e.Bounds.Height - iconSize) / 2;

            e.Graphics.DrawImage(bitmap, iconX, iconY, iconSize, iconSize);

            // 绘制文本，稍微偏右以避开图标
            string text = listBox.Items[e.Index].ToString();
            using (Brush textBrush = new SolidBrush(e.ForeColor))
            {
                e.Graphics.DrawString(text, e.Font, textBrush, iconX + iconSize + 5, e.Bounds.Top + 5);
            }

            e.DrawFocusRectangle();

        }

    }
}
