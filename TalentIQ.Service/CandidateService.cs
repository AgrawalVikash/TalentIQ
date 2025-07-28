using TalentIQ.Common.Models;
using TalentIQ.Repository.Interface;
using TalentIQ.Service.Interface;

namespace TalentIQ.Service
{
    public class CandidateService(ICandidateRepository repository) : ICandidateService
    {
        private readonly ICandidateRepository _repository = repository ?? throw new ArgumentNullException(nameof(repository));

        public Task<List<Candidate>> GetCandidatesAsync() => _repository.GetCandidatesAsync();

        public async Task<Candidate> AddCandidateAsync(CandidateUploadDto dto)
        {
            ArgumentNullException.ThrowIfNull(dto);
            if (dto.Resume == null || dto.Resume.Length == 0)
                throw new ArgumentNullException(nameof(dto.Resume), "Resume file is required.");

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
