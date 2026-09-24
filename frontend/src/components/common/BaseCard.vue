<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200">
    <div v-if="title" class="px-5 py-3 border-b border-gray-100 flex items-center justify-between">
      <h3 class="font-semibold text-gray-800">{{ title }}</h3>
      <slot name="actions" />
    </div>
    <div class="p-5">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String })
</script>