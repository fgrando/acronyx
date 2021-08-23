using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Text.RegularExpressions;

namespace Acronyx
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        // returns a list of unique acronyms alphabetically ordered
        private void listAcronyms(ref List<string> list)
        {
            string pattern = @"[A-Z0-9]{2,}";

            list.Clear();
            //string pattern = @"\b(([A-Z][A-Z]+)";
            Regex rgx = new Regex(pattern);

            foreach (Match match in rgx.Matches(this.richTextBoxInput.Text))
            {
                if (!list.Contains(match.Value))
                    list.Add(match.Value);
            }

            list.Sort();
        }

        private void renderTable(IDictionary<string, string> dic)
        {
            StringBuilder strTable = new StringBuilder();
            int cellWidth = 1000;

            this.richTextBoxOutput.Clear();

            strTable.Append(@"{\rtf1");

            foreach (KeyValuePair<string, string> acronym in dic)
            {
                strTable.Append(@"\trowd");

                strTable.Append(@"\cellx"+cellWidth.ToString()).AppendLine(acronym.Key);

                strTable.Append(@"\intbl\cell");

                strTable.Append(@"\cellx" + (2*cellWidth).ToString()).AppendLine(acronym.Value);

                strTable.Append(@"\intbl \cell \row");
            }

            strTable.Append(@"\pard");
            strTable.Append(@"}");

            richTextBoxOutput.Rtf = strTable.ToString();
        }

        private void process()
        {
            var acronyms = new List<string>();

            // get all acronyms from INPUT
            listAcronyms(ref acronyms);

            // list all finding in the EDIT
            Dictionary<string, string> dic = new Dictionary<string, string>();
            foreach (string acronym in acronyms)
            {
                Console.WriteLine(acronym);
                dataGridView1.Rows.Add(false, acronym, "XX");
                dic.Add(acronym, "XX\nYY");
            }

            // show output in TABLE
            renderTable(dic);
        }

        private void tabControl1_Selecting(object sender, TabControlCancelEventArgs e)
        {
            TabPage current = (sender as TabControl).SelectedTab;

            Console.WriteLine(current.Text);
            process();
        }

        private void richTextBoxInput_TextChanged(object sender, EventArgs e)
        {
            string txt = richTextBoxInput.Text;
            Console.WriteLine(txt);
            richTextBoxInput.Text = txt;
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {

        }

        private void loadToolStripMenuItem_Click(object sender, EventArgs e)
        {
            richTextBoxInput.Clear();
            richTextBoxInput.Text = "If you enable rich-text formatting for a rich text box, users can use a variety of options to format the text that they enter in that control.AFK Away From Keyboard BBIAB - Be Back In A Bit BBL - Be Back Later BBS - Be Back Soon EG - Evil Grin For example, they can apply a different font or character style to the text inside the rich text box or even insert a table into the rich text box.BEG Big Evil Grin.BRB - Be Right Back BTW By The Way. Depending on the options that you choose, users also may be able to link to or embed pictures in the rich text box.Embedding a picture stores the picture as part of the form and is a good choice if YOUR users don't need to update the picture. Linking to a picture stores the picture outside the form and is a better choice if you think that your users will need to update the linked picture, or if you want to reduce the file size of the completed form. If users link to a picture, they must have access to the location of the picture source file. Otherwise, the picture will not appear in the rich text box.";
        }
    }
}
