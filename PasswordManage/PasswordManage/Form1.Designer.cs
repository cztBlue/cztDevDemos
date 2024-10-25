using System.Drawing;
using System.Windows.Forms;
using System.Collections.Generic;

namespace PasswordManage
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改 sb
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.SuspendLayout();
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Name = "Form1";
            this.Text = "密码管理器";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);

        }

        #endregion

        private Panel panel { get; set; }
        /// <summary>
        /// 动态控件
        /// </summary>
        private void DynamicComponentGenerator() 
        {
            //panel
            panel = new Panel {
                Dock = DockStyle.Left,
                AutoScroll = true,
                Width = 300
            };
            int offsety = 10;

            Controls.Add(panel);
            var accountdata = new List<PasswordStruct>
            {
                new PasswordStruct() {Useraccount = "A",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "B",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "C",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "D",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
                new PasswordStruct() {Useraccount = "E",Password = "zxc123456"},
            };

            foreach (var item in accountdata)
            {
                Button button = new Button
                {
                    Text = item.Useraccount,
                    Location = new Point(10, offsety),
                    Width = 200,
                    Height = 30,
                    Margin = new Padding(0, 0, 0, 0), 
                };
                button.Click += (s, e) => Clipboard.SetText(item.Password);
                panel.Controls.Add(button);
                offsety += 30; // button的间距
            }

            //other ....
        }
    }
}

