using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TestExample
{
    public partial class YoIDE : Form
    {

        public String current_file = "";
        public String current_path = "";
        public String[] codezone_states = { };
        public int statecode;


        public YoIDE()
        {
            InitializeComponent();
        }

        private void Tm_file_exit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void Codezone_TextChanged(object sender, EventArgs e)
        {


            string[] keyWords = { "if", "else", "for", "def", "class" };
            Color orange = Color.FromArgb(255, 102, 0);
            find_keywords(keyWords, orange);

            string[] digits = { "1", "2", "3", "4", "5", "6", "7", "8", "9", "0" };
            Color blue = Color.FromArgb(100, 200, 255);
            find_keywords(digits, blue);

        }

        private void find_keywords(string[] keyWords, Color color)
        {
            int a = codezone.SelectionStart;

            foreach (string key in keyWords)
            {
                MatchCollection allKeyWords = Regex.Matches(codezone.Text, key);
                foreach (Match findKeyWord in allKeyWords)
                {
                    codezone.SelectionStart = findKeyWord.Index;
                    codezone.SelectionLength = findKeyWord.Length;
                    codezone.SelectionColor = color;
                }
            }
            codezone.SelectionStart = a;
            codezone.SelectionLength = 0;
            codezone.SelectionColor = codezone.ForeColor;
        }

        private void Tp_info_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Программное обеспечение создано компанией Dryandex.", "Справка");
        }


        private void newfileitem_Click(object sender, EventArgs e)
        {
            if (current_file.Length > 0)
            {
                // Сохраняем текущий файл
            }

            codezone.Clear();

            // Сохраняем во временное хранилище текущий файл
            // System.IO.File.WriteAllText(filename, textBox1.Text);

            filenamelabel.Text = "[Новый]";

        }

        private void СохранитьКакToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            if (saveFileDialog1.ShowDialog() == DialogResult.Cancel)
                return;
            // получаем выбранный файл
            string filename = saveFileDialog1.FileName;
            // сохраняем текст в файл
            System.IO.File.WriteAllText(filename, codezone.Text);

            current_path = get_pathfile(filename);
            current_file = get_filename(filename);
            MessageBox.Show("Файл сохранен");
            filenamelabel.Text = current_file;
        }

        private String get_filename(String url)
        {
            String[] array = url.Split('\\');
            String namefile = array[array.Length - 1];
            return namefile;
        }
        private String get_pathfile(String url)
        {
            String[] array = url.Split('\\');
            string[] strs = array.Take(array.Length - 1).ToArray();
            string path = string.Join("\\", strs);
            return path;
        }

        private void ОткрытьToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.Cancel)
                return;
            // получаем выбранный файл
            string filename = openFileDialog1.FileName;
            // читаем файл в строку
            string fileText = System.IO.File.ReadAllText(filename);
            codezone.Clear();
            codezone.Text = fileText;
            current_path = get_pathfile(filename);
            current_file = get_filename(filename);
            filenamelabel.Text = current_file;
        }

        private bool code_changed()
        {
            return codezone.Text == codezone_states[statecode];
        }


        private void СохранитьToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            

            if (filenamelabel.Text == "[Новый]")
            {
                
                if (saveFileDialog1.ShowDialog() == DialogResult.Cancel)
                    return;

                codezone_states = codezone_states.Concat(new string[] { codezone.Text }).ToArray();

                statecode = 0;

                string filename = saveFileDialog1.FileName;
                System.IO.File.WriteAllText(filename, codezone.Text);
                current_path = get_pathfile(filename);
                current_file = get_filename(filename);
                filenamelabel.Text = current_file;

            }
            else
            {
                codezone_states = codezone_states.Concat(new string[] { codezone.Text }).ToArray();
                statecode++;
                System.IO.File.WriteAllText(current_path + '\\' + current_file, codezone.Text);

            }
        }

        private void Undoitem_Click(object sender, EventArgs e)
        {

            if (statecode >= 0)
            {
                statecode--;
                update_codezone_state();
            }
            

        }

        private void Redoitem_Click(object sender, EventArgs e)
        {
            if (statecode < codezone_states.Length)
            {
                statecode++;
                update_codezone_state();
            }
        }

        private void update_codezone_state()
        {
            if (statecode >= 0 && statecode < codezone_states.Length)
            {
                codezone.Text = codezone_states[statecode];

            }
        }
    }
}
