using Microsoft.AspNetCore.Http;
using System.Text.Json;
using TalentIQ.Common.Models;
using TalentIQ.Common.Utils;
using TalentIQ.Repository.Interface;

namespace TalentIQ.Repository
{
    public class CandidateRepository : ICandidateRepository
    {
        private readonly string _jsonPath = Path.Combine("Data", "candidates.json");
        private readonly string _resumeFolder = Path.Combine("Uploads", "Resumes");

        public CandidateRepository()
        {
            var jsonDir = Path.GetDirectoryName(_jsonPath);
            if (!string.IsNullOrWhiteSpace(jsonDir))
                DirectoryHelper.EnsureDirectoryExists(jsonDir);

            DirectoryHelper.EnsureDirectoryExists(_resumeFolder);
        }

        public async Task<List<Candidate>> GetCandidatesAsync()
        {
            try
            {
                if (!File.Exists(_jsonPath)) return [];
                var json = await File.ReadAllTextAsync(_jsonPath).ConfigureAwait(false);
                return JsonSerializer.Deserialize<List<Candidate>>(json) ?? [];
            }
            catch (Exception ex)
            {
                // Log exception if logger available, or rethrow
                throw new IOException($"Failed to read candidates: {ex.Message}", ex);
            }
        }

        public async Task AddCandidateAsync(Candidate candidate)
        {
            if (candidate == null)
                throw new ArgumentNullException(nameof(candidate));

            try
            {
                var candidates = await GetCandidatesAsync().ConfigureAwait(false);
                candidates.Add(candidate);
                var json = JsonSerializer.Serialize(candidates, new JsonSerializerOptions { WriteIndented = true });
                await File.WriteAllTextAsync(_jsonPath, json).ConfigureAwait(false);
            }
            catch (Exception ex)
            {
                throw new IOException($"Failed to add candidate: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Saves a resume file asynchronously and returns the relative path.
        /// </summary>
        public async Task<string> SaveResumeAsync(IFormFile resume)
        {
            if (resume == null)
                throw new ArgumentNullException(nameof(resume));

            var fileName = $"{Guid.NewGuid()}_{Path.GetFileName(resume.FileName)}";
            var path = Path.Combine(_resumeFolder, fileName);

            try
            {
                using var stream = new FileStream(path, FileMode.Create, FileAccess.Write, FileShare.None, 4096, FileOptions.Asynchronous);
                await resume.CopyToAsync(stream).ConfigureAwait(false);
                // Return relative path for portability
                return Path.Combine("Uploads", "Resumes", fileName).Replace("\\", "/");
            }
            catch (Exception ex)
            {
                throw new IOException($"Failed to save resume: {ex.Message}", ex);
            }
        }
    }
}
