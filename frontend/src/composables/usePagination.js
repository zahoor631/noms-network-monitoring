import { computed, ref } from 'vue'

export function usePagination(items, perPage = 10) {
  const page = ref(1)
  const totalPages = computed(() => Math.ceil(items.value.length / perPage))
  const paginated = computed(() => {
    const start = (page.value - 1) * perPage
    return items.value.slice(start, start + perPage)
  })
  return { page, totalPages, paginated }
}