from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .catalog import PDF_DIR, ensure_dirs, list_pdf_files, load_catalog
from .models import (
    CatalogResponse,
    PdfImportResponse,
    SelectionRequest,
    SelectionResponse,
)
from .pdf_parser import import_all_pdfs
from .recommender import recommend, summarize_requirements

# 前端构建产物：单端口 http://127.0.0.1:8000 访问（国内推荐，无需翻墙）
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_dirs()
    yield


app = FastAPI(
    title="松下 CX 系列光电传感器选型 API",
    description="基于本地 PDF 样本与型号库的客户需求推荐服务",
    version="1.0.0",
    lifespan=lifespan,
)

# 开发模式（前后端分离）时的跨域；单端口模式不依赖外网
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    catalog = load_catalog()
    return {
        "status": "ok",
        "catalog_count": len(catalog),
        "pdf_count": len(list_pdf_files()),
        "frontend_bundled": (FRONTEND_DIST / "index.html").is_file(),
        "access_url": "http://127.0.0.1:8000",
    }


@app.get("/api/catalog", response_model=CatalogResponse)
def get_catalog() -> CatalogResponse:
    items = load_catalog()
    pdfs = list_pdf_files()
    source = "catalog.json"
    if pdfs:
        source += " + 本地 PDF"
    return CatalogResponse(items=items, source=source, pdf_files=pdfs)


@app.post("/api/recommend", response_model=SelectionResponse)
def post_recommend(req: SelectionRequest) -> SelectionResponse:
    catalog = load_catalog()
    if not catalog:
        return SelectionResponse(
            requirements_summary=summarize_requirements(req),
            recommendations=[],
            catalog_count=0,
        )
    recs = recommend(catalog, req)
    return SelectionResponse(
        requirements_summary=summarize_requirements(req),
        recommendations=recs,
        catalog_count=len(catalog),
    )


@app.post("/api/pdf/import", response_model=PdfImportResponse)
def post_pdf_import() -> PdfImportResponse:
    processed, found_count = import_all_pdfs()
    catalog = load_catalog()
    if not processed:
        return PdfImportResponse(
            message=f"请将 CX 系列 PDF 放入目录：{PDF_DIR}",
            files_processed=[],
            models_found=0,
            catalog_count=len(catalog),
        )
    return PdfImportResponse(
        message="PDF 解析完成，已合并至型号库",
        files_processed=processed,
        models_found=found_count,
        catalog_count=len(catalog),
    )


@app.post("/api/pdf/upload")
async def upload_pdf(file: UploadFile) -> dict:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return {"ok": False, "message": "仅支持 PDF 文件"}
    ensure_dirs()
    dest = PDF_DIR / file.filename
    content = await file.read()
    dest.write_bytes(content)
    processed, found_count = import_all_pdfs()
    return {
        "ok": True,
        "filename": file.filename,
        "files_processed": processed,
        "models_found": found_count,
        "catalog_count": len(load_catalog()),
    }


def _mount_frontend() -> None:
    index_file = FRONTEND_DIST / "index.html"
    if not index_file.is_file():

        @app.get("/", include_in_schema=False)
        async def frontend_not_built():
            return HTMLResponse(
                """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
                <title>请先构建前端</title></head><body style="font-family:sans-serif;padding:2rem">
                <h1>前端尚未构建</h1>
                <p>请在项目目录执行以下任一方式：</p>
                <ol>
                <li>双击运行 <b>安装依赖.bat</b></li>
                <li>或在 <code>frontend</code> 目录执行：<code>npm install</code> 然后 <code>npm run build</code></li>
                </ol>
                <p>构建完成后重启后端，再访问本页。</p>
                <p>API 文档：<a href="/docs">/docs</a> · 健康检查：<a href="/api/health">/api/health</a></p>
                </body></html>"""
            )

        return

    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(index_file)

    @app.get("/favicon.ico", include_in_schema=False)
    async def serve_favicon():
        favicon = FRONTEND_DIST / "favicon.ico"
        if favicon.is_file():
            return FileResponse(favicon)
        return FileResponse(index_file)


_mount_frontend()
