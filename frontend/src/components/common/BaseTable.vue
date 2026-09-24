<template>
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            class="text-left px-4 py-3 font-medium"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!rows.length">
          <td :colspan="columns.length" class="text-center py-8 text-gray-400">
            No data
          </td>
        </tr>
        <tr
          v-for="(row, i) in rows"
          :key="row.id || i"
          class="border-t border-gray-100 hover:bg-gray-50"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            class="px-4 py-3"
          >
            <slot :name="col.key" :row="row">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  columns: { type: Array, required: true }, // [{ key, label }]
  rows: { type: Array, default: () => [] },
})
</script>