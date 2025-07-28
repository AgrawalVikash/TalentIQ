using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
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
        private readonly ILogger<CandidateRepository> _logger;

        public CandidateRepository(ILogger<CandidateRepository> logger)
        {
            DirectoryHelper.EnsureDirectoryExists(Path.GetDirectoryName(_jsonPath)!);
            DirectoryHelper.EnsureDirectoryExists(_resumeFolder);
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        public async Task<List<Candidate>> GetCandidatesAsync()
        {
            try
            {
                if (!File.Exists(_jsonPath))
                {
                    _logger.LogInformation("Candidates file not found at {Path}. Returning empty list.", _jsonPath);
                    return [];
                }
                var json = await File.ReadAllTextAsync(_jsonPath).ConfigureAwait(false);
                var candidates = JsonSerializer.Deserialize<List<Candidate>>(json) ?? [];
                _logger.LogInformation("Retrieved {Count} candidates.", candidates.Count);
                return candidates;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to read candidates from {Path}", _jsonPath);
                throw new IOException($"Failed to read candidates: {ex.Message}", ex);
            }
        }

        public async Task AddCandidateAsync(Candidate candidate)
        {
            ArgumentNullException.ThrowIfNull(candidate);

            try
            {
                var candidates = await GetCandidatesAsync().ConfigureAwait(false);
                candidates.Add(candidate);
                var json = JsonSerializer.Serialize(candidates, new JsonSerializerOptions { WriteIndented = true });
                await File.WriteAllTextAsync(_jsonPath, json).ConfigureAwait(false);
                _logger.LogInformation("Added candidate {CandidateId} to {Path}", candidate.Id, _jsonPath);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to add candidate {CandidateId} to {Path}", candidate?.Id, _jsonPath);
                throw new IOException($"Failed to add candidate: {ex.Message}", ex);
            }
        }

        public async Task<string> SaveResumeAsync(IFormFile resume)
        {
            ArgumentNullException.ThrowIfNull(resume);

            var fileName = $"{Guid.NewGuid()}_{Path.GetFileName(resume.FileName)}";
            var path = Path.Combine(_resumeFolder, fileName);

            try
            {
                using var stream = new FileStream(path, FileMode.Create, FileAccess.Write, FileShare.None, 4096, FileOptions.Asynchronous);
                await resume.CopyToAsync(stream).ConfigureAwait(false);
                _logger.LogInformation("Saved resume file {FileName} to {Path}", fileName, path);
                return Path.Combine("Uploads", "Resumes", fileName).Replace("\\", "/");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to save resume {FileName} to {Path}", resume.FileName, path);
                throw new IOException($"Failed to save resume: {ex.Message}", ex);
            }
        }
    }
}
