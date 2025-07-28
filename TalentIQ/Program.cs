using Serilog;
using TalentIQ.Common.Utils;
using TalentIQ.Repository;
using TalentIQ.Repository.Interface;
using TalentIQ.Service;
using TalentIQ.Service.Interface;

var builder = WebApplication.CreateBuilder(args);

// Ensure log directory exists before logger setup
DirectoryHelper.EnsureDirectoryExists("logs");

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateLogger();

builder.Host.UseSerilog();

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Read CORS origins from appsettings.json
var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>();
if (allowedOrigins == null || allowedOrigins.Length == 0)
{
    allowedOrigins = ["http://localhost:4200"]; // fallback
}

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowTalentIQ", policy =>
    {
        policy.WithOrigins(allowedOrigins)
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Dependency Injection
builder.Services.AddScoped<ICandidateRepository, CandidateRepository>();
builder.Services.AddScoped<ICandidateService, CandidateService>();

var app = builder.Build();

// Global exception handler
app.UseExceptionHandler("/error");

// Enable Serilog request logging
app.UseSerilogRequestLogging();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("AllowTalentIQ");
app.UseAuthorization();
app.MapControllers();

app.Run();
