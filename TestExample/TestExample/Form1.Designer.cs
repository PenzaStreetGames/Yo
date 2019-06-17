namespace TestExample
{
    partial class YoIDE
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.newfileitem = new System.Windows.Forms.ToolStripMenuItem();
            this.открытьToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.сохранитьToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.сохранитьКакToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.tm_file_exit = new System.Windows.Forms.ToolStripMenuItem();
            this.сохранитьToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.redoitem = new System.Windows.Forms.ToolStripMenuItem();
            this.undoitem = new System.Windows.Forms.ToolStripMenuItem();
            this.вырезатьToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.копироватьToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.вставитьToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.найтиToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.сохранитьКакToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.стартToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.стопToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.следующийШагToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.предыдущийШагToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.настройкиToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.компиляцияToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.языкToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.кодировкаToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.tp_info = new System.Windows.Forms.ToolStripMenuItem();
            this.resultzone = new System.Windows.Forms.TextBox();
            this.codezone = new System.Windows.Forms.RichTextBox();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.filenamelabel = new System.Windows.Forms.Label();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripMenuItem1,
            this.сохранитьToolStripMenuItem,
            this.сохранитьКакToolStripMenuItem,
            this.настройкиToolStripMenuItem,
            this.tp_info});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(826, 24);
            this.menuStrip1.TabIndex = 1;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.newfileitem,
            this.открытьToolStripMenuItem,
            this.сохранитьToolStripMenuItem1,
            this.сохранитьКакToolStripMenuItem1,
            this.tm_file_exit});
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(48, 20);
            this.toolStripMenuItem1.Text = "Файл";
            // 
            // newfileitem
            // 
            this.newfileitem.Name = "newfileitem";
            this.newfileitem.Size = new System.Drawing.Size(180, 22);
            this.newfileitem.Text = "Новый";
            this.newfileitem.Click += new System.EventHandler(this.newfileitem_Click);
            // 
            // открытьToolStripMenuItem
            // 
            this.открытьToolStripMenuItem.Name = "открытьToolStripMenuItem";
            this.открытьToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.открытьToolStripMenuItem.Text = "Открыть";
            this.открытьToolStripMenuItem.Click += new System.EventHandler(this.ОткрытьToolStripMenuItem_Click);
            // 
            // сохранитьToolStripMenuItem1
            // 
            this.сохранитьToolStripMenuItem1.Name = "сохранитьToolStripMenuItem1";
            this.сохранитьToolStripMenuItem1.Size = new System.Drawing.Size(180, 22);
            this.сохранитьToolStripMenuItem1.Text = "Сохранить";
            this.сохранитьToolStripMenuItem1.Click += new System.EventHandler(this.СохранитьToolStripMenuItem1_Click);
            // 
            // сохранитьКакToolStripMenuItem1
            // 
            this.сохранитьКакToolStripMenuItem1.Name = "сохранитьКакToolStripMenuItem1";
            this.сохранитьКакToolStripMenuItem1.Size = new System.Drawing.Size(180, 22);
            this.сохранитьКакToolStripMenuItem1.Text = "Сохранить как";
            this.сохранитьКакToolStripMenuItem1.Click += new System.EventHandler(this.СохранитьКакToolStripMenuItem1_Click);
            // 
            // tm_file_exit
            // 
            this.tm_file_exit.Name = "tm_file_exit";
            this.tm_file_exit.Size = new System.Drawing.Size(180, 22);
            this.tm_file_exit.Text = "Выход";
            this.tm_file_exit.Click += new System.EventHandler(this.Tm_file_exit_Click);
            // 
            // сохранитьToolStripMenuItem
            // 
            this.сохранитьToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.redoitem,
            this.undoitem,
            this.вырезатьToolStripMenuItem,
            this.копироватьToolStripMenuItem,
            this.вставитьToolStripMenuItem,
            this.найтиToolStripMenuItem});
            this.сохранитьToolStripMenuItem.Name = "сохранитьToolStripMenuItem";
            this.сохранитьToolStripMenuItem.Size = new System.Drawing.Size(108, 20);
            this.сохранитьToolStripMenuItem.Text = "Редактирование";
            // 
            // redoitem
            // 
            this.redoitem.Name = "redoitem";
            this.redoitem.Size = new System.Drawing.Size(180, 22);
            this.redoitem.Text = "Шаг вперед";
            this.redoitem.Click += new System.EventHandler(this.Redoitem_Click);
            // 
            // undoitem
            // 
            this.undoitem.Name = "undoitem";
            this.undoitem.Size = new System.Drawing.Size(180, 22);
            this.undoitem.Text = "Шаг назад";
            this.undoitem.Click += new System.EventHandler(this.Undoitem_Click);
            // 
            // вырезатьToolStripMenuItem
            // 
            this.вырезатьToolStripMenuItem.Name = "вырезатьToolStripMenuItem";
            this.вырезатьToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.вырезатьToolStripMenuItem.Text = "Вырезать";
            // 
            // копироватьToolStripMenuItem
            // 
            this.копироватьToolStripMenuItem.Name = "копироватьToolStripMenuItem";
            this.копироватьToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.копироватьToolStripMenuItem.Text = "Копировать";
            // 
            // вставитьToolStripMenuItem
            // 
            this.вставитьToolStripMenuItem.Name = "вставитьToolStripMenuItem";
            this.вставитьToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.вставитьToolStripMenuItem.Text = "Вставить";
            // 
            // найтиToolStripMenuItem
            // 
            this.найтиToolStripMenuItem.Name = "найтиToolStripMenuItem";
            this.найтиToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.найтиToolStripMenuItem.Text = "Найти";
            // 
            // сохранитьКакToolStripMenuItem
            // 
            this.сохранитьКакToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.стартToolStripMenuItem,
            this.стопToolStripMenuItem,
            this.следующийШагToolStripMenuItem,
            this.предыдущийШагToolStripMenuItem});
            this.сохранитьКакToolStripMenuItem.Name = "сохранитьКакToolStripMenuItem";
            this.сохранитьКакToolStripMenuItem.Size = new System.Drawing.Size(64, 20);
            this.сохранитьКакToolStripMenuItem.Text = "Отладка";
            // 
            // стартToolStripMenuItem
            // 
            this.стартToolStripMenuItem.Name = "стартToolStripMenuItem";
            this.стартToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.стартToolStripMenuItem.Text = "Старт";
            // 
            // стопToolStripMenuItem
            // 
            this.стопToolStripMenuItem.Name = "стопToolStripMenuItem";
            this.стопToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.стопToolStripMenuItem.Text = "Стоп";
            // 
            // следующийШагToolStripMenuItem
            // 
            this.следующийШагToolStripMenuItem.Name = "следующийШагToolStripMenuItem";
            this.следующийШагToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.следующийШагToolStripMenuItem.Text = "Следующий шаг";
            // 
            // предыдущийШагToolStripMenuItem
            // 
            this.предыдущийШагToolStripMenuItem.Name = "предыдущийШагToolStripMenuItem";
            this.предыдущийШагToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            this.предыдущийШагToolStripMenuItem.Text = "Предыдущий шаг";
            // 
            // настройкиToolStripMenuItem
            // 
            this.настройкиToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.компиляцияToolStripMenuItem,
            this.языкToolStripMenuItem,
            this.кодировкаToolStripMenuItem});
            this.настройкиToolStripMenuItem.Name = "настройкиToolStripMenuItem";
            this.настройкиToolStripMenuItem.Size = new System.Drawing.Size(79, 20);
            this.настройкиToolStripMenuItem.Text = "Настройки";
            // 
            // компиляцияToolStripMenuItem
            // 
            this.компиляцияToolStripMenuItem.Name = "компиляцияToolStripMenuItem";
            this.компиляцияToolStripMenuItem.Size = new System.Drawing.Size(144, 22);
            this.компиляцияToolStripMenuItem.Text = "Компиляция";
            // 
            // языкToolStripMenuItem
            // 
            this.языкToolStripMenuItem.Name = "языкToolStripMenuItem";
            this.языкToolStripMenuItem.Size = new System.Drawing.Size(144, 22);
            this.языкToolStripMenuItem.Text = "Язык";
            // 
            // кодировкаToolStripMenuItem
            // 
            this.кодировкаToolStripMenuItem.Name = "кодировкаToolStripMenuItem";
            this.кодировкаToolStripMenuItem.Size = new System.Drawing.Size(144, 22);
            this.кодировкаToolStripMenuItem.Text = "Кодировка";
            // 
            // tp_info
            // 
            this.tp_info.Name = "tp_info";
            this.tp_info.Size = new System.Drawing.Size(65, 20);
            this.tp_info.Text = "Справка";
            this.tp_info.Click += new System.EventHandler(this.Tp_info_Click);
            // 
            // resultzone
            // 
            this.resultzone.BackColor = System.Drawing.SystemColors.InactiveCaptionText;
            this.resultzone.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.resultzone.ForeColor = System.Drawing.SystemColors.Window;
            this.resultzone.Location = new System.Drawing.Point(6, 429);
            this.resultzone.Multiline = true;
            this.resultzone.Name = "resultzone";
            this.resultzone.ReadOnly = true;
            this.resultzone.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.resultzone.ShortcutsEnabled = false;
            this.resultzone.Size = new System.Drawing.Size(813, 109);
            this.resultzone.TabIndex = 3;
            this.resultzone.WordWrap = false;
            // 
            // codezone
            // 
            this.codezone.AcceptsTab = true;
            this.codezone.BackColor = System.Drawing.SystemColors.InactiveCaptionText;
            this.codezone.Font = new System.Drawing.Font("Microsoft Sans Serif", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.codezone.ForeColor = System.Drawing.SystemColors.Menu;
            this.codezone.Location = new System.Drawing.Point(6, 53);
            this.codezone.Name = "codezone";
            this.codezone.ScrollBars = System.Windows.Forms.RichTextBoxScrollBars.ForcedBoth;
            this.codezone.ShortcutsEnabled = false;
            this.codezone.Size = new System.Drawing.Size(813, 367);
            this.codezone.TabIndex = 4;
            this.codezone.TabStop = false;
            this.codezone.Text = "";
            this.codezone.TextChanged += new System.EventHandler(this.Codezone_TextChanged);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // filenamelabel
            // 
            this.filenamelabel.AutoSize = true;
            this.filenamelabel.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.filenamelabel.Location = new System.Drawing.Point(8, 31);
            this.filenamelabel.Name = "filenamelabel";
            this.filenamelabel.Size = new System.Drawing.Size(47, 13);
            this.filenamelabel.TabIndex = 5;
            this.filenamelabel.Text = "[Новый]";
            // 
            // YoIDE
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(64)))), ((int)(((byte)(64)))), ((int)(((byte)(64)))));
            this.ClientSize = new System.Drawing.Size(826, 547);
            this.Controls.Add(this.filenamelabel);
            this.Controls.Add(this.codezone);
            this.Controls.Add(this.resultzone);
            this.Controls.Add(this.menuStrip1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MainMenuStrip = this.menuStrip1;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "YoIDE";
            this.Text = "YO IDE";
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem сохранитьToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem сохранитьКакToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem настройкиToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem tp_info;
        private System.Windows.Forms.ToolStripMenuItem открытьToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem сохранитьToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem сохранитьКакToolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem newfileitem;
        private System.Windows.Forms.ToolStripMenuItem tm_file_exit;
        private System.Windows.Forms.ToolStripMenuItem redoitem;
        private System.Windows.Forms.ToolStripMenuItem undoitem;
        private System.Windows.Forms.ToolStripMenuItem вырезатьToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem копироватьToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem вставитьToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem найтиToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem стартToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem стопToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem следующийШагToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem предыдущийШагToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem компиляцияToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem языкToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem кодировкаToolStripMenuItem;
        private System.Windows.Forms.TextBox resultzone;
        private System.Windows.Forms.RichTextBox codezone;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.Label filenamelabel;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
    }
}

