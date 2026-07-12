$ErrorActionPreference = "Stop"
Set-Location "c:\202444085_Assemble\simulation_contest2"

$jobs = @(
    @{
        App   = "PowerPoint"
        Src   = "피킹_프로세스_효율화_및_생산성_극대화_20260709235709.pptx"
        Dst   = "피킹_프로세스_효율화_및_생산성_극대화_20260709235709.pdf"
        Format = 32  # ppSaveAsPDF
    },
    @{
        App   = "Word"
        Src   = "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트보고서.docx"
        Dst   = "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트보고서.pdf"
        Format = 17  # wdFormatPDF
    },
    @{
        App   = "Word"
        Src   = "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트사용자매뉴얼.docx"
        Dst   = "제23회한국대학생컴퓨터시뮬레이션경진대회_인하이트사용자매뉴얼.pdf"
        Format = 17
    }
)

function Export-PptToPdf($src, $dst, $format) {
    $app = $null
    try {
        $app = New-Object -ComObject PowerPoint.Application
        $app.Visible = -1  # msoTrue
        $pres = $app.Presentations.Open($src, $true, $true, $false)
        $pres.SaveAs($dst, $format)
        $pres.Close()
        Write-Host "OK PPT -> $dst"
    }
    finally {
        if ($app) { $app.Quit() | Out-Null }
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
    }
}

function Export-WordToPdf($src, $dst, $format) {
    $app = $null
    try {
        $app = New-Object -ComObject Word.Application
        $app.Visible = $false
        $doc = $app.Documents.Open($src, $false, $true)
        $doc.ExportAsFixedFormat($dst, $format)
        $doc.Close($false)
        Write-Host "OK Word -> $dst"
    }
    finally {
        if ($app) { $app.Quit() | Out-Null }
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
    }
}

foreach ($job in $jobs) {
    $srcPath = (Resolve-Path $job.Src).Path
    $dstPath = Join-Path (Get-Location) $job.Dst
    if ($job.App -eq "PowerPoint") {
        Export-PptToPdf $srcPath $dstPath $job.Format
    }
    else {
        Export-WordToPdf $srcPath $dstPath $job.Format
    }
}

Write-Host "All PDF exports finished."
