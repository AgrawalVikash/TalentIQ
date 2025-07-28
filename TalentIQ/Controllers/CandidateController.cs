using Microsoft.AspNetCore.Mvc;
using TalentIQ.Common.Models;
using TalentIQ.Service.Interface;

namespace TalentIQ.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CandidateController(ICandidateService service, ILogger<CandidateController> logger) : ControllerBase
    {
        private readonly ICandidateService _service = service ?? throw new ArgumentNullException(nameof(service));
        private readonly ILogger<CandidateController> _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        [HttpGet("GetCandidateList")]
        public async Task<ActionResult<List<Candidate>>> GetCandidateList() => Ok(await _service.GetCandidatesAsync());

        [HttpPost("AddCandidate")]
        public async Task<ActionResult<Candidate>> AddCandidate([FromForm] CandidateUploadDto dto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            try
            {
                var candidate = await _service.AddCandidateAsync(dto);
                return Ok(candidate);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error adding candidate");
                return BadRequest(new { error = ex.Message });
            }
        }
    }
}
