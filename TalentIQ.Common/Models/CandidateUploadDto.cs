using Microsoft.AspNetCore.Http;

namespace TalentIQ.Common.Models
{
    public class CandidateUploadDto
    {
        public string Name { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public string JobId { get; set; } = string.Empty;
        public IFormFile Resume { get; set; } = default!;
    }
}
