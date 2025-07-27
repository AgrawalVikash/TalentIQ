namespace TalentIQ.Service.Utils
{
    public static class DirectoryHelper
    {
        public static void EnsureDirectoryExists(string filePath)
        {
            //var directory = Path.GetDirectoryName(filePath);
            if (!Directory.Exists(filePath))
            {
                Directory.CreateDirectory(filePath);
            }
        }
    }
}
