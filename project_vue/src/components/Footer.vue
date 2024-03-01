<template>
  <footer class="footer">
    <div class="container">
      <span class="text-muted">Your footer content goes here</span>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  width: 100%;
  background-color: black;
  padding: 10px 0;
  text-align: center;
  border-top: 1px solid #dee2e6;
  margin-top: auto; /* Push the footer to the bottom */
}

.container {
  max-width: 960px;
  margin: 0 auto;
}

.text-muted {
  color: #6c757d;
}
</style>
