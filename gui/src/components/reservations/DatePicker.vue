<template>
  <div class="lg:col-span-8">
    <div class="flex flex-col gap-12">
      <fieldset class="flex flex-col gap-2 animate-fade-up">
        <div class="flex items-baseline justify-between mb-1">
          <legend class="font-display text-[28px] leading-none">
            <span class="text-glow font-serif text-[30px] tracking-[0.14em] mr-3">02</span>
            Fechas de tu visita
          </legend>
          <span class="label-mono">Requerido</span>
        </div>
        <p class="text-[13.5px] text-bone-soft mb-4 max-w-[60ch]">
          Toca el día de entrada y luego el de salida. Los <span class="text-danger">martes están bloqueados</span>.
        </p>

        <!-- Calendar -->
        <div class="glass rounded-2xl p-5 md:p-6">
          <!-- Month tabs -->
          <div class="flex items-center justify-between mb-5">
            <div class="flex items-center gap-2">
              <button v-for="(m,i) in months" :key="i" 
                class="month-tab px-4 py-2 rounded-full font-mono text-[11px] tracking-[0.14em] uppercase text-[#9AA39E] cursor-pointer transition-all duration-200 ease-in-out border border-transparent hover:text-[#F4F1E8]" :class="{'is-on': monthIdx===i}" @click="monthIdx = i">
                {{ m.label }}
              </button>
            </div>
            <div class="hidden md:flex items-center gap-3 text-[11px] font-mono uppercase tracking-[0.14em] text-bone-soft">
              <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-(--color-accent)"></span>Selección</span>
              <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md border border-dashed border-[rgba(255,139,123,0.5)] bg-[rgba(255,139,123,0.06)]"></span>Martes</span>
            </div>
          </div>

          <!-- Calendar grid -->
          <div class="grid grid-cols-7 gap-1 mb-1">
            <div v-for="d in ['L','M','M','J','V','S','D']" :key="d" class="cal-head">{{ d }}</div>
          </div>
          <div class="grid grid-cols-7 gap-1">
            <div v-for="(c,i) in calendarCells" :key="i"
                  class="cal-cell"
                  :class="{
                    'is-other': c.other,
                    'is-blocked': c.blocked,
                    'is-disabled': c.disabled,
                    'is-today': c.today,
                    'is-in-range': c.inRange,
                    'is-start': c.isStart,
                    'is-end': c.isEnd,
                    'is-range': c.isStart && range.end || c.isEnd && range.start,
                  }"
                  @click="pickDate(c)">
              {{ c.day || '' }}
            </div>
          </div>

          <!-- Range summary -->
          <div class="hairline-flat mt-5 mb-4"></div>
          <div class="grid grid-cols-2 gap-3">
            <div class="px-4 py-3 rounded-xl bg-white/2 border border-white/5">
              <div class="label-mono">Entrada</div>
              <div class="text-[14px] mt-1.5">{{ range.start ? formatDate(range.start) : '— Selecciona —' }}</div>
            </div>
            <div class="px-4 py-3 rounded-xl bg-white/2 border border-white/5">
              <div class="label-mono">Salida</div>
              <div class="text-[14px] mt-1.5">{{ range.end ? formatDate(range.end) : '— Selecciona —' }}</div>
            </div>
          </div>
        </div>
      </fieldset>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from 'vue';
import { useReservationStore } from '../../stores/reservationStore.ts';

const store = useReservationStore();

const months = [
  { label:'Junio · 2026',  m:5, y:2026 },
  { label:'Julio · 2026',  m:6, y:2026 },
  { label:'Agosto · 2026', m:7, y:2026 },
];
const monthIdx = ref(0);
const range = reactive({
  start: store.llegada ? new Date(store.llegada) : null,
  end: store.salida ? new Date(store.salida) : null, 
});

watch(() => [range.start, range.end], ([start, end]) => {
  store.llegada = start ? start.toISOString().split('T')[0] : null;
  store.salida = end ? end.toISOString().split('T')[0] : null;
});

const calendarCells = computed(() => {
  const { m, y } = months[monthIdx.value];
  const first = new Date(y, m, 1);
  const last  = new Date(y, m+1, 0);
  const firstDay = (first.getDay() + 6) % 7;
  const totalDays = last.getDate();

  const cells = [];
  for (let i = 0; i < firstDay; i++) {
    cells.push({ other:true, disabled:true });
  }
  const today = new Date(); today.setHours(0,0,0,0);
  for (let d = 1; d <= totalDays; d++) {
    const date = new Date(y, m, d);
    const isTuesday = date.getDay() === 2;
    const isPast = date < today;
    cells.push({
      day: d,
      date,
      today: date.getTime() === today.getTime(),
      blocked: isTuesday,
      disabled: isPast && !isTuesday,
      isStart: range.start !== null && date.getTime() === range.start.getTime(),
      isEnd:   range.end !== null && date.getTime() === range.end.getTime(),
      inRange: range.start !== null && range.end !== null &&
                date > range.start && date < range.end,
    });
  }
  while (cells.length % 7 !== 0) cells.push({ other:true, disabled:true });

  return cells;
});

function pickDate(c: any) {
  if (!c.day || c.disabled || c.blocked) return;
  const d: Date = c.date;
  if (!range.start || range.end) {
    range.start = d;
    range.end = null;
    return;
  } else if (d.getTime() === range.start.getTime()) {
    range.start = null;
    range.end = null;
    return;
  } else if (d < range.start) {
    range.start = d;
    range.end = null;
    return;
  } 
  range.end = d;
}
function formatDate(d: Date | null) {
  if (!d) return '—';
  const days = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'];
  const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
  return `${days[d.getDay()]} ${d.getDate()} ${months[d.getMonth()]}`;
}
</script>

<style scoped>
.month-tab.is-on {
  background: rgba(232,255,122,0.1);
  border-color: rgba(232,255,122,0.3);
  color: var(--color-accent);
}

.cal-cell {
  aspect-ratio:1;
  border-radius:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:13px;
  color:#F4F1E8;
  cursor:pointer;
  position:relative;
  transition:all .15s ease;
  font-family:'Geist',sans-serif;
}
.cal-cell:hover:not(.is-disabled):not(.is-blocked) { background:rgba(244,241,232,0.06); }
.cal-cell.is-disabled {
  color: #3a4340;
  cursor: not-allowed;
}
.cal-cell.is-blocked {
  color: #5C645F;
  cursor: not-allowed;
  text-decoration: line-through;
  text-decoration-color: rgba(255,139,123,0.5);
}
.cal-cell.is-blocked::after {
  content: "";
  position: absolute;
  inset: 6px;
  border-radius: 8px;
  background: rgba(255,139,123,0.06);
  border: 1px dashed rgba(255,139,123,0.25);
  pointer-events: none;
}
.cal-cell.is-other { color:#3a4340; }
.cal-cell.is-today::before { 
  content: "";
  position: absolute;
  bottom: 4px; 
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  border-radius: 999px;
  background: var(--color-accent);
}
.cal-cell.is-in-range {
  background: rgba(232,255,122,0.08);
  border-radius: 0;
}
.cal-cell.is-start, .cal-cell.is-end {
  background: var(--color-accent);
  color: #07090A;
  font-weight: 600;
  box-shadow: 0 4px 18px -4px rgba(232,255,122,0.5);
  border-radius: 10px;
}
.cal-cell.is-start.is-range { border-radius:10px 0 0 10px; }
.cal-cell.is-end.is-range { border-radius:0 10px 10px 0; }
.cal-head { 
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: #5C645F;
  padding: 8px 0;
  text-align: center;
}

.hairline {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(244,241,232,0.16), transparent);
}
.hairline-flat {
  height: 1px;
  background: rgba(244,241,232,0.08);
}
</style>