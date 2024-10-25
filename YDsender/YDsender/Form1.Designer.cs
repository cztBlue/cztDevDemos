namespace YDsender
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
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.textBoxRaw = new System.Windows.Forms.TextBox();
            this.textBoxRes = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.work = new System.Windows.Forms.Button();
            this.btnstart = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // textBoxRaw
            // 
            this.textBoxRaw.Location = new System.Drawing.Point(95, 94);
            this.textBoxRaw.Name = "textBoxRaw";
            this.textBoxRaw.Size = new System.Drawing.Size(366, 25);
            this.textBoxRaw.TabIndex = 0;
            // 
            // textBoxRes
            // 
            this.textBoxRes.Location = new System.Drawing.Point(95, 171);
            this.textBoxRes.Name = "textBoxRes";
            this.textBoxRes.Size = new System.Drawing.Size(366, 25);
            this.textBoxRes.TabIndex = 1;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(23, 94);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(52, 15);
            this.label1.TabIndex = 2;
            this.label1.Text = "源文本";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(23, 171);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(67, 15);
            this.label2.TabIndex = 3;
            this.label2.Text = "翻译结果";
            // 
            // work
            // 
            this.work.Location = new System.Drawing.Point(541, 96);
            this.work.Name = "work";
            this.work.Size = new System.Drawing.Size(75, 23);
            this.work.TabIndex = 4;
            this.work.Text = "翻译";
            this.work.UseVisualStyleBackColor = true;
            this.work.Click += new System.EventHandler(this.work_Click);
            // 
            // btnstart
            // 
            this.btnstart.Location = new System.Drawing.Point(26, 12);
            this.btnstart.Name = "btnstart";
            this.btnstart.Size = new System.Drawing.Size(111, 33);
            this.btnstart.TabIndex = 5;
            this.btnstart.Text = "查看Session";
            this.btnstart.UseVisualStyleBackColor = true;
            this.btnstart.Click += new System.EventHandler(this.btnstart_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.btnstart);
            this.Controls.Add(this.work);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.textBoxRes);
            this.Controls.Add(this.textBoxRaw);
            this.Name = "Form1";
            this.Text = "有道网页翻译解密demo";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBoxRaw;
        private System.Windows.Forms.TextBox textBoxRes;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button work;
        private System.Windows.Forms.Button btnstart;
    }
}

