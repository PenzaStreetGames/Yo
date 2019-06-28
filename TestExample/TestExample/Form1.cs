using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Web.Script.Serialization;


namespace TestExample
{
    
    public partial class YoIDE : Form
    {

        public String current_file = "";
        public String current_path = "";
        public String[] codezone_states = { };
        public int statecode;


        private int[][] non_colored = { };
        private int[][] comment;
        private int[][] sign;
        private int[][] logic_value;
        private int[][] logic_operation;
        private int[][] number;
        private int[][] strings;
        private int[][] objects;
        private int[][] built_in_function;
        private int[][] structure;


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
            Json();

      

        }

        private void find_keywords(string[] keyWords, Color color)
        {
            
        }

        private void Tp_info_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Программное обеспечение создано компанией Dryandex.", "Справка");
        }

        private void Json()
        {
            int caretPosition = codezone.SelectionStart;

            codezone.SelectionStart = 0;
            codezone.SelectionLength = codezone.TextLength;
            codezone.SelectionColor = codezone.ForeColor;


            int a = codezone.SelectionStart;

            JavaScriptSerializer serializer = new JavaScriptSerializer();
            string baseDirectory = "";
            Console.WriteLine(baseDirectory);
            string json = File.ReadAllText(baseDirectory + "program.yohl");
            Dictionary<string, object> result = (Dictionary<string, object>)serializer.DeserializeObject(json);
            foreach(KeyValuePair<string, object> keyValue in result)
            {
                Array group = (Array)keyValue.Value;
                
                foreach (object subGroup in group)
                {
                    int row = 0, start = 0, end = 0;
                    Dictionary<string, object> elements = (Dictionary<string, object>)subGroup;
                    foreach(KeyValuePair<string, object> param in elements)
                    {
                        

                        if (param.Key == "row") {
                            row = int.Parse(param.Value.ToString());
                        }
                        if (param.Key == "begin")
                        {
                            start = int.Parse(param.Value.ToString());
                        }
                        if (param.Key == "end")
                        {
                            end = int.Parse(param.Value.ToString());
                        }
                        if (param.Key == "name")
                        {
                            //MessageBox.Show(param.Value.ToString());
                        }



                    }
                    String gr_name = $"{keyValue.Key}";

                    if (gr_name != "non_colored") {
                        int length = end - start + 1;

                        start += get_abs_symbol(row) + row;
                        codezone.SelectionStart = start;
                        codezone.SelectionLength = length;

                    
                        //MessageBox.Show(codezone.Text.Substring(start, length),  gr_name);
                        codezone.SelectionColor = get_color(gr_name);
                    }
                    
                }
            }

            codezone.SelectionStart = a;
            codezone.SelectionLength = 0;
            codezone.SelectionColor = codezone.ForeColor;

            codezone.SelectionStart = caretPosition;
            codezone.ScrollToCaret();
        }

        private int get_abs_symbol(int row)
        {
            String[] array = codezone.Text.Split('\n');
            int res = 0;
            for (int i = 0; i < row; i++)
            {
                res += array[i].Length;
            }
            return res;
        }

        private Color get_color(String gr)
        {
            Color res = Color.FromArgb(255, 255, 255);
            switch (gr)
            {
                case "non_colored":
                    res = Color.FromArgb(0, 0, 0);
                    break;
                case "comment":
                    res = Color.FromArgb(153, 153, 153);
                    break;
                case "sign":
                    res = Color.FromArgb(255, 207, 64);
                    break;
                case "logic_value":
                    res = Color.FromArgb(255, 117, 24);
                    break;
                case "logic_operation":
                    res = Color.FromArgb(204, 119, 34);
                    break;
                case "number":
                    res = Color.FromArgb(166, 202, 240);
                    break;
                case "strings":
                    res = Color.FromArgb(0, 125, 227);
                    break;
                case "objects":
                    res = Color.FromArgb(242, 221, 198);
                    break;
                case "built_in_function":
                    res = Color.FromArgb(34, 13, 0);
                    break;
                case "structure":
                    res = Color.FromArgb(253, 94, 83);
                    break;
               

            }
            return res;
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
