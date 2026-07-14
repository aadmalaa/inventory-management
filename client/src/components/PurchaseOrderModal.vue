<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen && backlogItem" class="modal-overlay" @click="close">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">
              {{ mode === 'view' ? t('purchaseOrder.viewTitle') : t('purchaseOrder.createTitle') }}
            </h3>
            <button class="close-button" @click="close">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <!-- Backlog item context (shown in both modes) -->
            <div class="context-card">
              <div class="context-grid">
                <div class="context-item">
                  <div class="context-label">{{ t('purchaseOrder.orderId') }}</div>
                  <div class="context-value order-id">{{ backlogItem.order_id }}</div>
                </div>
                <div class="context-item">
                  <div class="context-label">{{ t('purchaseOrder.sku') }}</div>
                  <div class="context-value sku">{{ backlogItem.item_sku }}</div>
                </div>
                <div class="context-item">
                  <div class="context-label">{{ t('purchaseOrder.itemName') }}</div>
                  <div class="context-value">{{ translateProductName(backlogItem.item_name) }}</div>
                </div>
                <div class="context-item">
                  <div class="context-label">{{ t('purchaseOrder.shortage') }}</div>
                  <div class="context-value shortage-value">{{ shortage }} {{ t('purchaseOrder.unitsShort') }}</div>
                </div>
              </div>
            </div>

            <!-- CREATE MODE: purchase order form -->
            <form v-if="mode === 'create'" class="po-form" @submit.prevent="handleSubmit">
              <div class="form-row">
                <div class="form-group flex-1">
                  <label for="po-supplier">{{ t('purchaseOrder.supplierName') }} *</label>
                  <input
                    id="po-supplier"
                    v-model="form.supplierName"
                    type="text"
                    :placeholder="t('purchaseOrder.supplierNamePlaceholder')"
                    class="po-input"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label for="po-quantity">{{ t('purchaseOrder.quantity') }} *</label>
                  <input
                    id="po-quantity"
                    v-model.number="form.quantity"
                    type="number"
                    min="1"
                    class="po-input"
                  />
                </div>

                <div class="form-group">
                  <label for="po-unit-cost">{{ t('purchaseOrder.unitCost') }} *</label>
                  <input
                    id="po-unit-cost"
                    v-model.number="form.unitCost"
                    type="number"
                    min="0.01"
                    step="0.01"
                    class="po-input"
                  />
                </div>

                <div class="form-group">
                  <label for="po-delivery-date">{{ t('purchaseOrder.expectedDeliveryDate') }} *</label>
                  <input
                    id="po-delivery-date"
                    v-model="form.expectedDeliveryDate"
                    type="date"
                    class="po-input"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group flex-1">
                  <label for="po-notes">{{ t('purchaseOrder.notes') }}</label>
                  <textarea
                    id="po-notes"
                    v-model="form.notes"
                    :placeholder="t('purchaseOrder.notesPlaceholder')"
                    class="po-textarea"
                    rows="3"
                  ></textarea>
                </div>
              </div>

              <div v-if="submitError" class="error-banner">{{ submitError }}</div>
            </form>

            <!-- VIEW MODE: read-only purchase order details -->
            <div v-else class="po-view">
              <div v-if="viewLoading" class="view-state">{{ t('purchaseOrder.loading') }}</div>
              <div v-else-if="viewError" class="view-state error-state">{{ viewError }}</div>
              <div v-else-if="viewPO" class="info-grid">
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.poId') }}</div>
                  <div class="info-value order-id">{{ viewPO.id }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.supplier') }}</div>
                  <div class="info-value">{{ viewPO.supplier_name }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.quantity') }}</div>
                  <div class="info-value">{{ viewPO.quantity }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.unitCost') }}</div>
                  <div class="info-value">{{ formatCurrencyWithDecimals(viewPO.unit_cost, selectedCurrency, 2) }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.total') }}</div>
                  <div class="info-value total-value">{{ formatCurrencyWithDecimals(total, selectedCurrency, 2) }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.expectedDeliveryDate') }}</div>
                  <div class="info-value">{{ formatDate(viewPO.expected_delivery_date) }}</div>
                </div>
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.status') }}</div>
                  <div class="info-value">
                    <span class="badge status-badge">{{ viewPO.status }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <div class="info-label">{{ t('purchaseOrder.createdDate') }}</div>
                  <div class="info-value">{{ formatDate(viewPO.created_date) }}</div>
                </div>
                <div v-if="viewPO.notes" class="info-item full-width">
                  <div class="info-label">{{ t('purchaseOrder.notes') }}</div>
                  <div class="info-value notes-value">{{ viewPO.notes }}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="close">
              {{ mode === 'create' ? t('purchaseOrder.cancel') : t('common.close') }}
            </button>
            <button
              v-if="mode === 'create'"
              class="btn-primary"
              :disabled="!isFormValid || saving"
              @click="handleSubmit"
            >
              {{ saving ? t('purchaseOrder.submitting') : t('purchaseOrder.submit') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'
import { formatCurrencyWithDecimals } from '../utils/currency'

const { t, currentCurrency, currentLocale, translateProductName } = useI18n()
const selectedCurrency = currentCurrency

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  backlogItem: {
    type: Object,
    default: null
  },
  mode: {
    type: String,
    default: 'create'
  }
})

const emit = defineEmits(['close', 'po-created'])

const shortage = computed(() => {
  if (!props.backlogItem) return 0
  return props.backlogItem.quantity_needed - props.backlogItem.quantity_available
})

// Create-mode form state
const form = ref({
  supplierName: '',
  quantity: 1,
  unitCost: null,
  expectedDeliveryDate: '',
  notes: ''
})
const saving = ref(false)
const submitError = ref(null)

// View-mode state
const viewPO = ref(null)
const viewLoading = ref(false)
const viewError = ref(null)

const total = computed(() => {
  if (!viewPO.value) return 0
  return viewPO.value.quantity * viewPO.value.unit_cost
})

const isFormValid = computed(() => {
  return form.value.supplierName.trim().length > 0 &&
    Number(form.value.quantity) > 0 &&
    Number(form.value.unitCost) > 0 &&
    !!form.value.expectedDeliveryDate
})

const resetForm = () => {
  form.value = {
    supplierName: '',
    // Default quantity to the shortage amount so the buyer covers the gap by default
    quantity: shortage.value > 0 ? shortage.value : 1,
    unitCost: null,
    expectedDeliveryDate: '',
    notes: ''
  }
  submitError.value = null
  saving.value = false
}

const loadExistingPO = async () => {
  if (!props.backlogItem) return

  // Prefer the PO already embedded on the backlog item to avoid an extra request
  if (props.backlogItem.purchase_order) {
    viewPO.value = props.backlogItem.purchase_order
    viewError.value = null
    return
  }

  viewPO.value = null
  viewLoading.value = true
  viewError.value = null
  try {
    viewPO.value = await api.getPurchaseOrderByBacklogItem(props.backlogItem.id)
  } catch (err) {
    viewError.value = err.response?.data?.detail || err.message || t('purchaseOrder.loadError')
  } finally {
    viewLoading.value = false
  }
}

// Re-initialize whenever the modal is opened for a (possibly new) backlog item/mode
watch(
  () => [props.isOpen, props.mode, props.backlogItem?.id],
  ([isOpen, mode]) => {
    if (!isOpen) return
    if (mode === 'view') {
      loadExistingPO()
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  if (!isFormValid.value || saving.value || !props.backlogItem) return

  saving.value = true
  submitError.value = null

  const payload = {
    backlog_item_id: props.backlogItem.id,
    supplier_name: form.value.supplierName.trim(),
    quantity: Number(form.value.quantity),
    unit_cost: Number(form.value.unitCost),
    expected_delivery_date: form.value.expectedDeliveryDate
  }
  if (form.value.notes.trim()) {
    payload.notes = form.value.notes.trim()
  }

  try {
    const created = await api.createPurchaseOrder(payload)
    emit('po-created', created)
  } catch (err) {
    submitError.value = err.response?.data?.detail || err.message || t('purchaseOrder.createError')
  } finally {
    saving.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  // Guard against invalid/unparseable dates before calling date methods
  if (isNaN(date.getTime())) return 'N/A'
  const locale = currentLocale.value === 'ja' ? 'ja-JP' : 'en-US'
  return date.toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.close-button {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.close-button:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.context-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
}

.context-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.context-item {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.context-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}

.context-value {
  font-size: 0.938rem;
  color: #0f172a;
  font-weight: 500;
}

.context-value.order-id,
.context-value.sku {
  font-family: 'Monaco', 'Courier New', monospace;
  color: #2563eb;
}

.context-value.shortage-value {
  color: #dc2626;
  font-weight: 700;
}

.po-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.form-group.flex-1 {
  flex: 1;
}

label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
}

.po-input,
.po-textarea {
  padding: 0.625rem 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.938rem;
  font-family: inherit;
  color: #0f172a;
  transition: border-color 0.15s ease;
}

.po-input:focus,
.po-textarea:focus {
  outline: none;
  border-color: #3b82f6;
}

.po-textarea {
  resize: vertical;
}

.error-banner {
  padding: 0.75rem 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #991b1b;
  font-size: 0.875rem;
}

.po-view {
  min-height: 80px;
}

.view-state {
  padding: 2rem;
  text-align: center;
  color: #64748b;
  font-size: 0.938rem;
}

.view-state.error-state {
  color: #dc2626;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-label {
  font-size: 0.813rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}

.info-value {
  font-size: 0.938rem;
  color: #0f172a;
  font-weight: 500;
}

.info-value.order-id {
  font-family: 'Monaco', 'Courier New', monospace;
  color: #2563eb;
}

.info-value.total-value {
  font-weight: 700;
  color: #0f172a;
}

.notes-value {
  white-space: pre-wrap;
}

.badge.status-badge {
  display: inline-block;
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.813rem;
  font-weight: 600;
  text-transform: capitalize;
  background: #dbeafe;
  color: #1e40af;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn-secondary {
  padding: 0.625rem 1.25rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.875rem;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: inherit;
}

.btn-secondary:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
}

.btn-primary {
  padding: 0.625rem 1.25rem;
  background: #3b82f6;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  color: white;
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: inherit;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.2s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}
</style>
