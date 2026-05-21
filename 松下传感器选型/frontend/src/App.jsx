import { useCallback, useEffect, useState } from "react";

const DETECTION_TYPES = [
  { value: "auto", label: "自动（由系统根据距离等推断）" },
  { value: "through_beam", label: "透过型" },
  { value: "retro_reflective", label: "回归反射型" },
  { value: "diffuse_reflective", label: "扩散反射型" },
  { value: "distance_set", label: "距离设定反射型" },
  { value: "limited_reflective", label: "限定反射型" },
];

const DISTANCE_PRESETS = [
  { label: "100 mm", mm: 100 },
  { label: "300 mm", mm: 300 },
  { label: "800 mm", mm: 800 },
  { label: "1 m", mm: 1000 },
  { label: "3 m", mm: 3000 },
  { label: "10 m", mm: 10000 },
];

const defaultForm = {
  detection_type: "auto",
  detection_distance_mm: 500,
  transparent_object: false,
  small_spot: false,
  narrow_beam: false,
  pcb_detection: false,
  oil_resistant: false,
  output_type: "any",
  top_n: 5,
};

export default function App() {
  const [form, setForm] = useState(defaultForm);
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState("");
  const [health, setHealth] = useState(null);
  const [result, setResult] = useState(null);

  const loadHealth = useCallback(async () => {
    try {
      const res = await fetch("/api/health");
      if (res.ok) setHealth(await res.json());
    } catch {
      setHealth(null);
    }
  }, []);

  useEffect(() => {
    loadHealth();
  }, [loadHealth]);

  const update = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handleRecommend = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          detection_distance_mm: Number(form.detection_distance_mm),
          top_n: Number(form.top_n),
        }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "推荐请求失败");
      }
      setResult(await res.json());
    } catch (err) {
      setError(err.message || "无法连接后端，请先启动 API 服务（端口 8000）");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleImportPdfs = async () => {
    setImporting(true);
    setError("");
    try {
      const res = await fetch("/api/pdf/import", { method: "POST" });
      const data = await res.json();
      alert(data.message + (data.files_processed?.length ? `\n已处理：${data.files_processed.join(", ")}` : ""));
      await loadHealth();
    } catch (err) {
      setError(err.message);
    } finally {
      setImporting(false);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setImporting(true);
    setError("");
    const body = new FormData();
    body.append("file", file);
    try {
      const res = await fetch("/api/pdf/upload", { method: "POST", body });
      const data = await res.json();
      if (!data.ok) throw new Error(data.message);
      alert(`已上传并解析：${data.filename}\n型号库共 ${data.catalog_count} 条`);
      await loadHealth();
    } catch (err) {
      setError(err.message);
    } finally {
      setImporting(false);
      e.target.value = "";
    }
  };

  return (
    <div className="app">
      <header>
        <h1>松下 CX 系列光电传感器选型</h1>
        <p>根据客户需求从本地 PDF 样本与型号库中推荐合适型号</p>
      </header>

      <div className="layout">
        <div className="card">
          <h2>客户需求</h2>
          <form onSubmit={handleRecommend}>
            <div className="field">
              <label htmlFor="detection_type">检测方式</label>
              <select
                id="detection_type"
                value={form.detection_type}
                onChange={(e) => update("detection_type", e.target.value)}
              >
                {DETECTION_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label htmlFor="distance">所需检测距离</label>
              <input
                id="distance"
                type="number"
                min={1}
                value={form.detection_distance_mm}
                onChange={(e) => update("detection_distance_mm", e.target.value)}
              />
              <div style={{ marginTop: 8, display: "flex", flexWrap: "wrap", gap: 6 }}>
                {DISTANCE_PRESETS.map((p) => (
                  <button
                    key={p.mm}
                    type="button"
                    className="secondary"
                    style={{ padding: "4px 10px", fontSize: "0.8rem" }}
                    onClick={() => update("detection_distance_mm", p.mm)}
                  >
                    {p.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="field">
              <label>输出类型</label>
              <select
                value={form.output_type}
                onChange={(e) => update("output_type", e.target.value)}
              >
                <option value="any">不限</option>
                <option value="npn">NPN</option>
                <option value="pnp">PNP</option>
              </select>
            </div>

            <div className="field checks">
              <label>
                <input
                  type="checkbox"
                  checked={form.transparent_object}
                  onChange={(e) => update("transparent_object", e.target.checked)}
                />
                检测透明物体（玻璃、薄膜、PET 等）
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={form.small_spot}
                  onChange={(e) => update("small_spot", e.target.checked)}
                />
                需要小光点 / 细小工件
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={form.narrow_beam}
                  onChange={(e) => update("narrow_beam", e.target.checked)}
                />
                窄视角 / 狭长检测区域
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={form.pcb_detection}
                  onChange={(e) => update("pcb_detection", e.target.checked)}
                />
                PCB / SMT 基板检测
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={form.oil_resistant}
                  onChange={(e) => update("oil_resistant", e.target.checked)}
                />
                油雾、冷却液或 IP67 环境
              </label>
            </div>

            <div className="actions">
              <button type="submit" className="primary" disabled={loading}>
                {loading ? "推荐中…" : "获取型号推荐"}
              </button>
            </div>
          </form>

          <div className="pdf-section">
            <strong>本地 PDF 数据</strong>
            <p style={{ fontSize: "0.85rem", color: "#607d8b", margin: "6px 0" }}>
              将松下 CX 系列样本 PDF 放入后端 data/pdfs 目录，或在此上传
            </p>
            <input type="file" accept=".pdf" onChange={handleUpload} disabled={importing} />
            <div className="actions" style={{ marginTop: 10 }}>
              <button
                type="button"
                className="secondary"
                disabled={importing}
                onClick={handleImportPdfs}
              >
                {importing ? "处理中…" : "重新扫描 PDF 目录"}
              </button>
            </div>
          </div>

          {health && (
            <div className="status-bar">
              型号库 {health.catalog_count} 条 · 本地 PDF {health.pdf_count} 个
            </div>
          )}
          {error && <div className="error">{error}</div>}
        </div>

        <div className="card">
          <h2>推荐结果</h2>
          {!result && (
            <div className="empty">填写左侧需求后点击「获取型号推荐」</div>
          )}
          {result && (
            <>
              <div className="summary">
                <strong>需求摘要：</strong>
                {result.requirements_summary}
              </div>
              {result.recommendations.length === 0 ? (
                <div className="empty">无匹配型号，请导入 PDF 或调整条件</div>
              ) : (
                <div className="rec-list">
                  {result.recommendations.map((rec, i) => (
                    <div key={rec.product.model_base} className="rec-item">
                      <span className="rank">推荐 #{i + 1}</span>
                      <h3>{rec.product.model_base}</h3>
                      <div className="model">订货型号：{rec.recommended_model}</div>
                      <div className="meta">
                        {rec.product.detection_type_label} · 检测距离{" "}
                        {rec.product.detection_distance_text} · {rec.product.light_source}
                      </div>
                      <div className="score">匹配得分：{rec.score}</div>
                      <ul>
                        {rec.reasons.map((r) => (
                          <li key={r}>{r}</li>
                        ))}
                      </ul>
                      {rec.product.features?.length > 0 && (
                        <div className="meta" style={{ marginTop: 6 }}>
                          特点：{rec.product.features.join("、")}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
