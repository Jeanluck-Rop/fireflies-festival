<template>
  <div class="searchbar">

    <!-- Campo de texto principal (siempre visible si hay un filtro text) -->
    <div v-if="textFilter" class="search-input-wrapper">
      <svg class="search-icon" width="14" height="14" viewBox="0 0 14 14" fill="none">
        <circle cx="6" cy="6" r="4.5" stroke="currentColor" stroke-width="1.4"/>
        <path d="M9.5 9.5l3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
      </svg>
      <input
        :value="modelValue[textFilter.key] ?? ''"
        :placeholder="textFilter.placeholder ?? 'Buscar...'"
        class="search-input"
        @input="update(textFilter!.key, ($event.target as HTMLInputElement).value)"
      />
      <button
        v-if="modelValue[textFilter.key]"
        class="search-clear"
        @click="update(textFilter!.key, '')">
	<IconClear size="22px"/>
      </button>
    </div>

    <!-- Filtros adicionales -->
    <div v-if="extraFilters.length" class="filters-row">
      <template v-for="filter in extraFilters" :key="filter.key">

        <!-- Select -->
        <div v-if="filter.type === 'select'" class="filter-chip-wrapper">
          <select
            :value="modelValue[filter.key] ?? ''"
            class="filter-select"
            @change="update(filter.key, ($event.target as HTMLSelectElement).value)">
            <option value="">{{ filter.placeholder ?? 'Todos' }}</option>
            <option
              v-for="opt in filter.options"
              :key="opt.value"
	      :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
          <svg class="select-chevron" width="10" height="10" viewBox="0 0 10 10" fill="none">
            <path d="M2 3.5l3 3 3-3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
        </div>

        <!-- Date simple -->
        <div v-else-if="filter.type === 'date'" class="filter-chip-wrapper">
          <input
            :value="modelValue[filter.key] ?? ''"
            type="date"
            class="filter-date"
            :placeholder="filter.placeholder ?? 'Fecha'"
            @change="update(filter.key, ($event.target as HTMLInputElement).value)"
          />
        </div>

        <!-- Daterange, dos campos -->
        <div v-else-if="filter.type === 'daterange'" class="filter-daterange">
          <input
            :value="modelValue[filter.key + '_desde'] ?? ''"
            type="date"
            class="filter-date"
            @change="update(filter.key + '_desde', ($event.target as HTMLInputElement).value)"
          />
	  <IconArrow class="daterange-sep" />
          <input
            :value="modelValue[filter.key + '_hasta'] ?? ''"
            type="date"
            class="filter-date"
            @change="update(filter.key + '_hasta', ($event.target as HTMLInputElement).value)"
          />
        </div>

        <!-- Number -->
        <div v-else-if="filter.type === 'number'" class="filter-chip-wrapper">
          <input
            :value="modelValue[filter.key] ?? ''"
            type="number"
            :placeholder="filter.placeholder ?? '0'"
            class="filter-number"
            @input="update(filter.key, ($event.target as HTMLInputElement).value)"
          />
        </div>
      </template>

      <!-- Boton limpiar todos los filtros -->
      <button
        v-if="hasActiveFilters"
        class="clear-all"
        @click="clearAll">
        Limpiar filtros
      </button>

    </div>

  </div>
</template>

<script setup lang="ts">
 import { computed } from 'vue'
 import IconClear from '../svg/IconClear.vue'
 import IconArrow from '../svg/IconArrow.vue'

 //Tipos publicos, exportados para que los usen las views
 export type FilterType = 'text' | 'select' | 'date' | 'daterange' | 'number'

 export interface FilterDef {
   key:          string
   type:         FilterType
   placeholder?: string
   options?:     { label: string; value: string }[]
 }

 export type FilterValues = Record<string, string>

 //Props y emits
 const props = defineProps<{
   filters:    FilterDef[]
   modelValue: FilterValues
 }>()

 const emit = defineEmits<{
   'update:modelValue': [value: FilterValues]
 }>()

 //Separar filtro text principal del resto
 const textFilter = computed(() =>
   props.filters.find(f => f.type === 'text') ?? null
 )

 const extraFilters = computed(() =>
   props.filters.filter(f => f.type !== 'text')
 )

 //Detectar si hay filtros activos
 const hasActiveFilters = computed(() =>
   Object.values(props.modelValue).some(v => v !== '' && v != null)
 )

 //Actualizar un campo del v-model
 function update(key: string, value: string) {
   emit('update:modelValue', { ...props.modelValue, [key]: value })
 }

 //Limpiar todo
 function clearAll() {
   const empty: FilterValues = {}
   props.filters.forEach(f => {
     if (f.type === 'daterange') {
       empty[f.key + '_desde'] = ''
       empty[f.key + '_hasta'] = ''
     } else {
       empty[f.key] = ''
     }
   })
   emit('update:modelValue', empty)
 }
</script>

<style scoped>
 .searchbar {
   display: flex;
   flex-direction: column;
   gap: 0.6rem;
 }

 /* Input de texto principal */
 .search-input-wrapper {
   position: relative;
   width: 100%;
 }

 .search-icon {
   position: absolute;
   left: 14px;
   top: 50%;
   transform: translateY(-50%);
   color: var(--color-bone-mute);
   pointer-events: none;
 }

 .search-input {
   width: 100%;
   height: 40px;
   padding: 0 2.5rem 0 2.5rem;
   border-radius: 999px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04);
   color: var(--color-bone);
   font-size: 13px;
   font-family: var(--font-sans);
   outline: none;
   transition: border-color 0.2s, background 0.2s;
 }
 .search-input::placeholder { color: var(--color-bone-mute) }
 .search-input:focus {
   border-color: rgba(123,216,176,0.4);
   background: rgba(255,255,255,0.06);
 }

 .search-clear {
   position: absolute;
   right: 12px;
   top: 50%;
   transform: translateY(-50%);
   background: none;
   border: none;
   color: var(--color-bone-mute);
   cursor: pointer;
   display: flex;
   align-items: center;
   padding: 2px;
   transition: color 0.2s;
 }
 .search-clear:hover { color: var(--color-bone-soft) }

 /* Fila de filtros extra */
 .filters-row {
   display: flex;
   flex-wrap: wrap;
   align-items: center;
   gap: 0.5rem;
 }

 /* Select */
 .filter-chip-wrapper {
   position: relative;
   display: flex;
   align-items: center;
 }

 .filter-select {
   height: 32px;
   padding: 0 2rem 0 0.85rem;
   border-radius: 999px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04);
   color: var(--color-bone);
   font-size: 12px;
   font-family: var(--font-sans);
   outline: none;
   appearance: none;
   cursor: pointer;
   transition: border-color 0.2s;
 }
 .filter-select:focus { border-color: rgba(123,216,176,0.4) }

 .select-chevron {
   position: absolute;
   right: 8px;
   color: var(--color-bone-mute);
   pointer-events: none;
 }

 /* Date */
 .filter-date {
   height: 32px;
   padding: 0 0.85rem;
   border-radius: 999px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04);
   color: var(--color-bone);
   font-size: 12px;
   font-family: var(--font-sans);
   outline: none;
   cursor: pointer;
   transition: border-color 0.2s;
   color-scheme: dark;
 }
 .filter-date:focus { border-color: rgba(123,216,176,0.4) }

 /* Daterange */
 .filter-daterange {
   display: flex;
   align-items: center;
   gap: 0.4rem;
 }

 .daterange-sep {
   font-size: 11px;
   color: var(--color-bone-mute);
 }

 /* Number */
 .filter-number {
   height: 32px;
   width: 110px;
   padding: 0 0.85rem;
   border-radius: 999px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04);
   color: var(--color-bone);
   font-size: 12px;
   font-family: var(--font-sans);
   outline: none;
   transition: border-color 0.2s;
 }
 .filter-number:focus { border-color: rgba(123,216,176,0.4) }

 /* Limpiar todo */
 .clear-all {
   height: 32px;
   padding: 0 0.85rem;
   border-radius: 999px;
   border: 1px solid rgba(255,138,123,0.25);
   background: transparent;
   color: var(--color-danger);
   font-size: 12px;
   font-family: var(--font-sans);
   cursor: pointer;
   transition: background 0.2s, border-color 0.2s;
   white-space: nowrap;
 }
 .clear-all:hover {
   background: rgba(255,138,123,0.08);
   border-color: rgba(255,138,123,0.4);
 }
 .daterange-sep {
   color: var(--color-bone-mute);
   display: flex;
   align-items: center;
 }
</style>
