using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace cztBlueTools.WorkHandler
{
    internal class ParseInputHandler
    {
        public ParseInputHandler() { }

        /// <summary>
        /// 把(111,222,xxxx,...)这样的坐标解析为数组
        /// </summary>
        /// <param name="input"></param>
        /// <returns></returns>
        public static int[] ParsePointInt(string input) 
        {
            var input_ = input;

            input_ = input_.Trim('(', ')');

            string[] numberStrings = input_.Split(',');

            int[] numbers = Array.ConvertAll(numberStrings, int.Parse);

            return numbers;
        }
        public static double[] ParsePointDouble(string input) 
        {
            var input_ = input;

            input_ = input_.Trim('(', ')');

            string[] numberStrings = input_.Split(',');

            double[] numbers = Array.ConvertAll(numberStrings, double.Parse);

            return numbers;
        }


    }
}
