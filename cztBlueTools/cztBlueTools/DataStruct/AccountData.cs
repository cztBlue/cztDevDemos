using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.StartPanel;

namespace cztBlueTools.DataStruct
{
    internal class AccountData
    {
        //必填
        public string BelongTo { get; set; }
        public string Account { get; set; }
        public string Password { get; set; }
        //选填
        public string UserName { get; set; }
        public string Domain { get; set; }
        public string Email { get; set; }
        public string Phone { get; set; }
        public string Append1 { get; set; }
        public string Append2 { get; set; }
        public string Append3 { get; set; }

        public AccountData(string belong,
                        string account,
                        string passsword,
                        string userName = "",
                        string domain = "",
                        string email = "",
                        string phone = "",
                        string append1 = "",
                        string append2 = "",
                        string append3 = "")
        {
            BelongTo = belong;
            Account = account;
            Password = passsword;
            UserName = userName;
            Domain = domain;
            Email = email;
            Phone = phone;
            Append1 = append1;
            Append2 = append2;
            Append3 = append3;

        }

    }
}
