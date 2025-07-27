using Microsoft.AspNetCore.Mvc;
using TalentIQ.Common.Models;
using TalentIQ.Service.Interface;

namespace TalentIQ.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CandidateController(ICandidateService service, ILogger<CandidateController> logger) : ControllerBase
    {
        private readonly ICandidateService _service = service;
        private readonly ILogger<CandidateController> _logger = logger;
        //private readonly string _jsonPath = Path.Combine("Data", "candidates.json");
        //private readonly string _uploadFolder = Path.Combine("Uploads", "Resumes");

        [HttpGet("GetCandidateList")]
        public async Task<IActionResult> GetCandidateList() => Ok(await _service.GetCandidatesAsync());

        [HttpPost("AddCandidate")]
        public async Task<IActionResult> AddCandidate([FromForm] CandidateUploadDto dto)
        {
            try
            {
                var candidate = await _service.AddCandidateAsync(dto);
                return Ok(candidate);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }


        //[HttpGet]
        //public IActionResult GetCandidates()
        //{
        //    if (!System.IO.File.Exists(_jsonPath))
        //        return Ok(new List<object>());

        //    var data = System.IO.File.ReadAllText(_jsonPath);
        //    return Ok(JsonSerializer.Deserialize<List<Candidate>>(data));
        //}

        //[HttpPost]
        //public async Task<IActionResult> AddCandidate([FromForm] CandidateUploadModel model)
        //{
        //    if (model.Resume == null) return BadRequest("Resume file required");

        //    Directory.CreateDirectory(_uploadFolder);
        //    var filePath = Path.Combine(_uploadFolder, $"{Guid.NewGuid()}_{model.Resume.FileName}");
        //    using var stream = new FileStream(filePath, FileMode.Create);
        //    await model.Resume.CopyToAsync(stream);

        //    var candidate = new Candidate
        //    {
        //        Id = Guid.NewGuid(),
        //        Name = model.Name,
        //        Email = model.Email,
        //        Phone = model.Phone,
        //        JobId = model.JobId,
        //        ResumePath = filePath.Replace("\\", "/"),
        //        Status = "Pending",
        //        CreatedAt = DateTime.UtcNow
        //    };

        //    List<Candidate> candidates = new();
        //    if (System.IO.File.Exists(_jsonPath))
        //    {
        //        var json = System.IO.File.ReadAllText(_jsonPath);
        //        candidates = JsonSerializer.Deserialize<List<Candidate>>(json) ?? new();
        //    }
        //    candidates.Add(candidate);

        //    System.IO.File.WriteAllText(_jsonPath, JsonSerializer.Serialize(candidates, new JsonSerializerOptions { WriteIndented = true }));

        //    return Ok(candidate);
        //}
    }

    //public class CandidateUploadModel
    //{
    //    public string Name { get; set; }
    //    public string Email { get; set; }
    //    public string Phone { get; set; }
    //    public string JobId { get; set; }
    //    public IFormFile Resume { get; set; }
    //}

    //public class Candidate
    //{
    //    public Guid Id { get; set; }
    //    public string Name { get; set; }
    //    public string Email { get; set; }
    //    public string Phone { get; set; }
    //    public string JobId { get; set; }
    //    public string ResumePath { get; set; }
    //    public string Status { get; set; }
    //    public DateTime CreatedAt { get; set; }
    //}
}
