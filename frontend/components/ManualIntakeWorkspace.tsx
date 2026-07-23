"use client";

import {
  AlertCircle,
  CheckCircle2,
  Link,
  ListPlus,
  LoaderCircle,
  RefreshCw,
} from "lucide-react";
import { FormEvent, useCallback, useEffect, useState } from "react";
import type { ManualIntakeBatch, ManualIntakeStatus } from "../lib/api";

const statusLabels: Record<ManualIntakeStatus, string> = {
  draft: "Черновик",
  queued: "В очереди",
  processing: "Обрабатывается",
  analyzed: "Проанализировано",
  failed: "Ошибка",
};

type ApiError = {
  detail?: string | Array<{ msg?: string }>;
};

async function readResponse<T>(response: Response): Promise<T> {
  const payload = (await response.json().catch(() => null)) as ApiError | T | null;
  if (response.ok) {
    return payload as T;
  }

  const detail = (payload as ApiError | null)?.detail;
  if (typeof detail === "string") {
    throw new Error(detail);
  }
  if (Array.isArray(detail)) {
    throw new Error(detail.map((item) => item.msg).filter(Boolean).join(". "));
  }
  throw new Error(`Ошибка запроса: ${response.status}`);
}

export default function ManualIntakeWorkspace() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [urlText, setUrlText] = useState("");
  const [batches, setBatches] = useState<ManualIntakeBatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const loadBatches = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch("/api/manual-intake/batches", {
        cache: "no-store",
      });
      setBatches(await readResponse<ManualIntakeBatch[]>(response));
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Не удалось загрузить подборки",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadBatches();
  }, [loadBatches]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setMessage("");

    const urls = urlText
      .split(/\r?\n/)
      .map((url) => url.trim())
      .filter(Boolean);

    if (!name.trim() || urls.length === 0) {
      setError("Укажите название и хотя бы одну ссылку.");
      return;
    }
    if (urls.length > 100) {
      setError("За один раз можно добавить не более 100 ссылок.");
      return;
    }
    if (new Set(urls).size !== urls.length) {
      setError("Удалите повторяющиеся ссылки.");
      return;
    }

    setSubmitting(true);
    try {
      const response = await fetch("/api/manual-intake/batches", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          name: name.trim(),
          description: description.trim() || null,
          urls,
        }),
      });
      const created = await readResponse<ManualIntakeBatch>(response);
      setBatches((current) => [
        created,
        ...current.filter((batch) => batch.id !== created.id),
      ]);
      setName("");
      setDescription("");
      setUrlText("");
      setMessage(`Подборка «${created.name}» добавлена.`);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Не удалось добавить подборку",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="dashboard-panel manual-panel">
      <div className="toolbar">
        <div>
          <h1>Ручная подборка</h1>
          <p>
            Добавьте найденные вами объявления. Система проверит источник и
            сохранит ссылки в очереди для дальнейшего анализа.
          </p>
        </div>
        <div className="toolbar-note">
          <ListPlus size={16} />
          Добавлено вручную
        </div>
      </div>

      <div className="manual-intake-grid">
        <form className="manual-form" onSubmit={handleSubmit}>
          <label>
            <span>Название подборки</span>
            <input
              maxLength={255}
              onChange={(event) => setName(event.target.value)}
              placeholder="Например: Объекты СЗАО от инвестора"
              required
              type="text"
              value={name}
            />
          </label>
          <label>
            <span>Комментарий (необязательно)</span>
            <input
              maxLength={2000}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Что важно проверить в этой подборке"
              type="text"
              value={description}
            />
          </label>
          <label>
            <span>Ссылки на объявления, по одной в строке</span>
            <textarea
              onChange={(event) => setUrlText(event.target.value)}
              placeholder={"https://www.cian.ru/sale/commercial/...\nhttps://www.avito.ru/..."}
              required
              rows={6}
              value={urlText}
            />
          </label>
          <button disabled={submitting} type="submit">
            {submitting ? (
              <LoaderCircle className="manual-spin" size={17} />
            ) : (
              <ListPlus size={17} />
            )}
            {submitting ? "Добавляем..." : "Добавить в анализ"}
          </button>
          <div aria-live="polite">
            {error && (
              <p className="manual-feedback manual-feedback-error">
                <AlertCircle size={16} />
                {error}
              </p>
            )}
            {message && (
              <p className="manual-feedback manual-feedback-success">
                <CheckCircle2 size={16} />
                {message}
              </p>
            )}
          </div>
        </form>

        <div className="manual-batch-list">
          <div className="manual-list-head">
            <strong>Последние подборки</strong>
            <button
              aria-label="Обновить список"
              className="manual-refresh"
              disabled={loading}
              onClick={() => void loadBatches()}
              title="Обновить список"
              type="button"
            >
              <RefreshCw className={loading ? "manual-spin" : ""} size={17} />
            </button>
          </div>
          {loading && batches.length === 0 ? (
            <p className="manual-empty">Загружаем подборки...</p>
          ) : null}
          {!loading && batches.length === 0 && !error ? (
            <p className="manual-empty">Подборок пока нет.</p>
          ) : null}
          {batches.map((batch) => (
            <article className="manual-batch-card" key={batch.id}>
              <div className="manual-batch-head">
                <div>
                  <h2>{batch.name}</h2>
                  {batch.description ? <p>{batch.description}</p> : null}
                </div>
                <span className={`manual-status manual-status-${batch.status}`}>
                  {statusLabels[batch.status]}
                </span>
              </div>
              <div className="manual-batch-metrics">
                <span>
                  <strong>{batch.total_urls}</strong>
                  ссылок
                </span>
                <span>
                  <strong>{batch.analyzed_count}</strong>
                  проанализировано
                </span>
                <span>
                  <strong>{Math.max(batch.total_urls - batch.processed_count, 0)}</strong>
                  ожидает анализа
                </span>
              </div>
              <div className="manual-url-preview">
                {batch.urls.slice(0, 3).map((item) => (
                  <span key={item.id} title={item.error_message ?? item.url}>
                    <Link size={14} />
                    {item.source_detected || "unknown"} · {statusLabels[item.status]}
                  </span>
                ))}
              </div>
              <small>
                Создано: {new Date(batch.created_at).toLocaleString("ru-RU")}
              </small>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
