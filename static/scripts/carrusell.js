let currentSlide = 0;

function updateIndicators() {
  const indicators = document.querySelectorAll('.indicator');
  indicators.forEach((indicator, index) => {
    indicator.classList.toggle('active', index === currentSlide);
  });
}

function goToSlide(index) {
  const carouselInner = document.getElementById('carouselInner');
  const totalSlides = document.querySelectorAll('.carousel-item').length;
  currentSlide = (index + totalSlides) % totalSlides;
  carouselInner.style.transform = `translateX(-${currentSlide * 100}%)`;
  updateIndicators();
}

function nextSlide() {
  goToSlide(currentSlide + 1);
}

function prevSlide() {
  goToSlide(currentSlide - 1);
}