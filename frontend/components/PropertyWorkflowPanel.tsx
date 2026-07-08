import { ClipboardList, FileText, History, PencilLine } from "lucide-react";
import type { DashboardProperty } from "../lib/api";

function formatDate(value: string) {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

export function PropertyWorkflowPanel({ property }: { property: DashboardProperty }) {
  const overrides = Object.entries(property.manual_overrides ?? {});
  const history = property.correction_history ?? [];
  const documents = property.requested_documents ?? [];

  return (
    <div className="workflow-panel">
      <div className="workflow-status-row">
        <span className={`workflow-status workflow-status-${property.property_workflow_status ?? "new"}`}>
          Статус: {property.property_workflow_status_label ?? "Новый"}
        </span>
        <p>
          <strong>Следующий шаг:</strong> {property.workflow_next_action ?? "Проверить исходные данные объявления."}
        </p>
      </div>

      <div className="workflow-grid">
        <div className="workflow-block">
          <h4>
            <PencilLine size={16} />
            Ручные уточнения
          </h4>
          {overrides.length > 0 ? (
            <div className="override-list">
              {overrides.map(([field, override]) => (
                <article className="override-card" key={field}>
                  <strong>{override.label}</strong>
                  <div className="override-change">
                    <span>{override.original_value}</span>
                    <span>→</span>
                    <span>{override.override_value}</span>
                  </div>
                  <p>Источник: {override.source}</p>
                  <p>Комментарий: {override.comment}</p>
                  <small>{formatDate(override.updated_at)}</small>
                </article>
              ))}
            </div>
          ) : (
            <p className="muted">Ручных уточнений пока нет.</p>
          )}
        </div>

        <div className="workflow-block">
          <h4>
            <History size={16} />
            История изменений
          </h4>
          {history.length > 0 ? (
            <div className="history-list">
              {history.map((item) => (
                <article className="history-item" key={`${item.field}-${item.changed_at}`}>
                  <strong>{formatDate(item.changed_at)} — {item.label}</strong>
                  <p>{item.old_value} → {item.new_value}</p>
                  <small>Источник: {item.source}</small>
                </article>
              ))}
            </div>
          ) : (
            <p className="muted">История изменений пока пуста.</p>
          )}
        </div>
      </div>

      <div className="workflow-block">
        <h4>
          <FileText size={16} />
          Документы
        </h4>
        {documents.length > 0 ? (
          <div className="document-list">
            {documents.map((document) => (
              <article className={`document-card document-status-${document.status}`} key={document.title}>
                <div>
                  <strong>{document.title}</strong>
                  <p>{document.comment}</p>
                </div>
                <span>{document.status_label}</span>
              </article>
            ))}
          </div>
        ) : (
          <p className="muted">Документы еще не запрошены.</p>
        )}
      </div>

      <div className="workflow-note">
        <ClipboardList size={16} />
        Данные в этом блоке sample-only: сохранение правок, пользователи и загрузка документов будут добавлены позже.
      </div>
    </div>
  );
}
