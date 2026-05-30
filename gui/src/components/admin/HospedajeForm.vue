<template>
  <div class="hosp-form">

    <!-- Tipo + Categoria + Estado -->
    <div class="form-row-3">
      <div class="field-group">
        <label class="field-label">Tipo</label>
        <div class="tipo-group">
          <button :class="['tipo-btn', form.tipo === 'CABANA' && 'active']"    @click="form.tipo = 'CABANA'">Cabaña</button>
          <button :class="['tipo-btn', form.tipo === 'CAMPING' && 'active']"   @click="form.tipo = 'CAMPING'">Camping</button>
        </div>
      </div>
      <div class="field-group">
        <label class="field-label">Categoría</label>
        <select v-model="form.categoria" class="form-select">
          <option value="INDIVIDUAL">Individual</option>
          <option value="PAREJA">Pareja</option>
          <option value="FAMILIAR">Familiar</option>
        </select>
      </div>
      <div v-if="showEstado" class="field-group">
        <label class="field-label">Estado</label>
        <select v-model="form.estado" class="form-select">
          <option value="DISPONIBLE">Disponible</option>
          <option value="MANTENIMIENTO">Mantenimiento</option>
        </select>
      </div>
    </div>

    <!-- Capacidad + Precio -->
    <div class="form-row-2">
      <div class="field-group">
        <label class="field-label">Capacidad (personas)</label>
        <input v-model.number="form.capacidad" type="number" min="1" class="form-input" />
      </div>
      <div class="field-group">
        <label class="field-label">Precio por noche (MXN)</label>
        <input v-model.number="form.precio" type="number" min="0" class="form-input" />
      </div>
    </div>

    <!-- Camas + Banos (solo cabana) -->
    <div v-if="form.tipo === 'CABANA'" class="form-row-2">
      <div class="field-group">
        <label class="field-label">Número de camas</label>
        <input v-model.number="form.num_camas" type="number" min="0" class="form-input" />
      </div>
      <div class="field-group">
        <label class="field-label">Número de baños</label>
        <input v-model.number="form.num_banos" type="number" min="0" class="form-input" />
      </div>
    </div>

    <!-- Amenidades -->
    <div v-if="form.tipo === 'CABANA'" class="field-group">
      <label class="field-label">Amenidades</label>
      <div class="amenidades-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="form.tiene_agua" />
          Agua potable
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="form.tiene_luz" />
          Electricidad
        </label>
        <label class="checkbox-label">
          <input type="checkbox" v-model="form.tiene_regadera" />
          Regadera
        </label>
      </div>
    </div>

    <!-- Descripcion -->
    <div class="field-group">
      <label class="field-label">Descripción</label>
      <textarea v-model="form.descripcion" class="form-input form-textarea" rows="2" placeholder="Descripción del hospedaje"/>
    </div>

    <!-- Imagenes -->
    <div class="field-group">
      <label class="field-label">Imágenes</label>
      <div class="images-gallery">
        <div v-for="(img, idx) in localImages" :key="idx" class="img-thumb">
          <img :src="img.url" alt="imagen" />
	  <button class="img-remove" @click="localImages.splice(idx, 1)">
	    <IconCross size="8px" />
	  </button>
        </div>
        <label class="img-add">
          <input type="file" accept="image/*" multiple style="display:none" @change="addImages" />
          <span>+</span>
        </label>
      </div>
    </div>

    <!-- Acciones -->
    <div class="form-actions">
      <slot name="extra-actions" />
      <div class="actions-right">
        <button class="btn-cancel" @click="$emit('cancel')">Cancelar</button>
        <button class="btn-save" :disabled="saving" @click="$emit('save')">
          {{ saving ? 'Guardando...' : 'Guardar' }}
        </button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
 import { ref } from 'vue'
 import IconCross from '../svg/IconCross.vue'

 const props = defineProps<{
   form: any
   saving?: boolean
   showEstado?: boolean
 }>()

 defineEmits<{ save: []; cancel: [] }>()

 const localImages = ref<{ url: string }[]>([])

 function addImages(e: Event) {
   const files = (e.target as HTMLInputElement).files
   if (!files) return
   Array.from(files).forEach(file => {
     const reader = new FileReader()
     reader.onload = ev => localImages.value.push({ url: ev.target?.result as string })
     reader.readAsDataURL(file)
     // TODO backend: POST /api/hospedajes/{id}/imagenes/
   })
 }
</script>

<style scoped>
 .hosp-form { display: flex; flex-direction: column; gap: 0.875rem; }

 .form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
 .form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.75rem; }

 .field-group { display: flex; flex-direction: column; gap: 0.3rem; }
 .field-label {
   font-size: 10.5px; font-family: var(--font-mono);
   text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-bone-mute);
 }

 .form-input, .form-select {
   height: 38px; padding: 0 0.75rem; border-radius: 8px;
   border: 1px solid var(--color-border); background: rgba(255,255,255,0.04);
   color: var(--color-bone); font-size: 13px; font-family: var(--font-sans);
   outline: none; width: 100%; transition: border-color 0.2s;
 }
 .form-input:focus, .form-select:focus { border-color: rgba(123,167,212,0.4); }
 .form-select { appearance: none; cursor: pointer; }
 .form-textarea { height: auto; min-height: 60px; resize: vertical; padding: 0.5rem 0.75rem; }

 .tipo-group { display: flex; gap: 0.4rem; }
 .tipo-btn {
   flex: 1; height: 38px; border-radius: 8px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); font-size: 12.5px; cursor: pointer; transition: all 0.15s;
 }
 .tipo-btn.active {
   border-color: var(--color-admin-accent, #7BA7D4);
   background: rgba(123,167,212,0.12);
   color: var(--color-admin-accent, #7BA7D4);
 }

 .amenidades-group { display: flex; gap: 1.25rem; flex-wrap: wrap; }
 .checkbox-label {
   display: flex; align-items: center; gap: 0.4rem;
   font-size: 12.5px; color: var(--color-bone-soft); cursor: pointer;
 }
 .checkbox-label input { cursor: pointer; accent-color: var(--color-admin-accent, #7BA7D4); }

 .images-gallery { display: flex; flex-wrap: wrap; gap: 0.5rem; }
 .img-thumb {
   position: relative; width: 64px; height: 64px;
   border-radius: 6px; overflow: hidden; border: 1px solid var(--color-border);
 }
 .img-thumb img { width: 100%; height: 100%; object-fit: cover; }
 .img-remove {
   position: absolute; top: 2px; right: 2px;
   width: 18px; height: 18px; border-radius: 50%;
   background: rgba(0,0,0,0.65); border: none; color: #fff;
   font-size: 13px; cursor: pointer; display: flex; align-items: center; justify-content: center;
 }
 .img-add {
   width: 64px; height: 64px; border-radius: 6px;
   border: 1px dashed rgba(123,167,212,0.3);
   display: flex; align-items: center; justify-content: center;
   cursor: pointer; color: var(--color-admin-accent, #7BA7D4);
   font-size: 22px; transition: background 0.15s;
 }
 .img-add:hover { background: rgba(123,167,212,0.06); }

 .form-actions { display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; margin-top: 0.25rem; flex-wrap: wrap; }
 .actions-right { display: flex; gap: 0.5rem; }
 .btn-cancel {
   height: 34px; padding: 0 1rem; border-radius: 999px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); font-size: 12.5px; cursor: pointer;
 }
 .btn-save {
   height: 34px; padding: 0 1.25rem; border-radius: 999px; border: none;
   background: var(--color-admin-accent, #7BA7D4); color: #0A1525;
   font-size: 12.5px; font-weight: 600; cursor: pointer;
 }
 .btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
