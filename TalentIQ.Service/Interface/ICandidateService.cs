using TalentIQ.Common.Models;

namespace TalentIQ.Service.Interface
{
    public interface ICandidateService
    {
        Task<List<Candidate>> GetCandidatesAsync();
        Task<Candidate> AddCandidateAsync(CandidateUploadDto dto);
    }
}
