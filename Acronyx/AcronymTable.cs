using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace Acronyx
{
    class AcronymTable
    {
        Dictionary<string, string> definitions = new Dictionary<string, string>();
        Dictionary<string, string> current = new Dictionary<string, string>();

        public void build(List<string> acronyms)
        {
            foreach (string acronym in acronyms)
            {
                current.Add(acronym, "XX\nYY");
            }
        }
        public IDictionary<string, string> toDictionary()
        {
            return current;
        }

        public bool saveDic(string filepath)
        {
            Console.WriteLine("saving dic to " + filepath);
            System.IO.File.WriteAllText(filepath, "test");
            return true;
        }
        public bool loadDic(string filepath)
        {
            Console.WriteLine("loading dic from " + filepath);
            string text = System.IO.File.ReadAllText(filepath);
            return true;
        }
    }
}
