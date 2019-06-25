using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web.Script.Serialization;
using System.IO;

namespace YoCSharpJson
{
    class Program
    {
        static void Main(string[] args)
        {
            JavaScriptSerializer serializer = new JavaScriptSerializer();
            string baseDirectory = "E:/PenzaStreetCompany/Python/-Yo-/yotranslator";
            Console.WriteLine(baseDirectory);
            string json = File.ReadAllText(baseDirectory + "/program.yohl");
            Dictionary<string, object> result = (Dictionary<string, object>)serializer.DeserializeObject(json);
            foreach(KeyValuePair<string, object> keyValue in result)
            {
                Array group = (Array)keyValue.Value;
                Console.WriteLine($"{keyValue.Key} {group}");
                foreach(object subGroup in group)
                {
                    Dictionary<string, object> elements = (Dictionary<string, object>)subGroup;
                    foreach(KeyValuePair<string, object> param in elements)
                    {
                        Console.WriteLine($"{param.Key} {param.Value}");
                    }
                    Console.WriteLine();
                }
                Console.WriteLine();
            }
            Console.ReadKey();
        }
    }
}
