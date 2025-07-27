using Microsoft.AspNetCore.Http;
using System.Text.Json;
using TalentIQ.Common.Models;
using TalentIQ.Repository.Interface;
using TalentIQ.Service.Utils;

namespace TalentIQ.Repository
{
    public class CandidateRepository : ICandidateRepository
    {
        private readonly string _jsonPath = Path.Combine("Data", "candidates.json");
        private readonly string _resumeFolder = Path.Combine("Uploads", "Resumes");

        public CandidateRepository()
        {
            DirectoryHelper.EnsureDirectoryExists(Path.GetDirectoryName(_jsonPath)!);
            DirectoryHelper.EnsureDirectoryExists(_resumeFolder);
        }

        public async Task<List<Candidate>> GetCandidatesAsync()
        {
            if (!File.Exists(_jsonPath)) return [];
            var json = await File.ReadAllTextAsync(_jsonPath);
            return JsonSerializer.Deserialize<List<Candidate>>(json) ?? [];
        }

        public async Task AddCandidateAsync(Candidate candidate)
        {
            var candidates = await GetCandidatesAsync();
            candidates.Add(candidate);
            var json = JsonSerializer.Serialize(candidates, new JsonSerializerOptions { WriteIndented = true });
            await File.WriteAllTextAsync(_jsonPath, json);
        }

        public async Task<string> SaveResumeAsync(IFormFile resume)
        {
            var fileName = $"{Guid.NewGuid()}_{resume.FileName}";
            var path = Path.Combine(_resumeFolder, fileName);
            using var stream = new FileStream(path, FileMode.Create);
            await resume.CopyToAsync(stream);
            return path.Replace("\\", "/");
        }
    }
}
