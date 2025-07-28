using Microsoft.Extensions.Logging;
using TalentIQ.Common.Models;
using TalentIQ.Repository.Interface;
using TalentIQ.Service.Interface;

namespace TalentIQ.Service
{
    public class CandidateService(ICandidateRepository repository, ILogger<CandidateService> logger) : ICandidateService
    {
        private readonly ICandidateRepository _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        private readonly ILogger<CandidateService> _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        public async Task<List<Candidate>> GetCandidatesAsync()
        {
            try
            {
                var candidates = await _repository.GetCandidatesAsync().ConfigureAwait(false);
                _logger.LogInformation("Retrieved {Count} candidates.", candidates.Count);
                return candidates;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving candidates.");
                throw;
            }
        }

        public async Task<Candidate> AddCandidateAsync(CandidateUploadDto dto)
        {
            ArgumentNullException.ThrowIfNull(dto);
            if (dto.Resume == null || dto.Resume.Length == 0)
            {
                ArgumentNullException argumentNullException = new(nameof(dto.Resume), "Resume file is required.");
                throw argumentNullException;
            }

            var resumePath = await _repository.SaveResumeAsync(dto.Resume).ConfigureAwait(false);

            var candidate = new Candidate
            {
                Id = Guid.NewGuid(),
                Name = dto.Name,
                Email = dto.Email,
                Phone = dto.Phone,
                JobId = dto.JobId,
                ResumePath = resumePath,
                CreatedAt = DateTime.UtcNow
            };

            await _repository.AddCandidateAsync(candidate).ConfigureAwait(false);
            return candidate;
        }
    }
}
