/* ----------------------------------------------------------------
   PROFESSIONAL SCHOOL SITE JAVASCRIPT
   Author: Gemini Model
   Purpose: Interactive features, animations, and responsive menu handling.
---------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Mobile Menu Toggle ---
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.querySelector('i').classList.toggle('fa-bars');
            menuToggle.querySelector('i').classList.toggle('fa-xmark');
        });
    }


    // --- 2. Scroll Reveal Animation ---
    const revealElements = document.querySelectorAll('.reveal');

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;

        revealElements.forEach(el => {
            // Get the top position of the element relative to the viewport
            const elementTop = el.getBoundingClientRect().top;
            const revealPoint = 150; // Offset in pixels

            // If the element is within the viewport (with an offset)
            if (elementTop < windowHeight - revealPoint) {
                el.classList.add('active');
            } else {
                // Optional: remove 'active' class when scrolling up
                // el.classList.remove('active');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Run once on load to show elements already in view


    // --- 3. Home Page Hero Image Slider ---
    const heroSection = document.querySelector('.hero[data-bg-images]');

    if (heroSection) {
        const images = JSON.parse(heroSection.dataset.bgImages);
        let currentSlide = 0;

        // Function to create and insert a slide element
        const createSlide = (imageUrl, index) => {
            const slide = document.createElement('div');
            slide.classList.add('hero-slide');
            if (index === 0) {
                slide.classList.add('active');
            }
            slide.style.backgroundImage = `url(${imageUrl})`;
            heroSection.appendChild(slide);
            return slide;
        };

        const slides = images.map(createSlide);

        const nextSlide = () => {
            // Hide current slide
            slides[currentSlide].classList.remove('active');

            // Determine next slide index
            currentSlide = (currentSlide + 1) % slides.length;

            // Show next slide
            slides[currentSlide].classList.add('active');
        };

        // Start the slideshow (Change every 6 seconds)
        setInterval(nextSlide, 6000);
    }


    // --- 4. Testimonials Slider ---
    const sliderContainer = document.querySelector('.testimonial-slider');

    if (sliderContainer) {
        const slider = sliderContainer.querySelector('.test-slides');
        const slides = sliderContainer.querySelectorAll('.slide');
        const prevBtn = sliderContainer.querySelector('.tprev');
        const nextBtn = sliderContainer.querySelector('.tnext');
        let currentIndex = 0;

        const updateSlider = () => {
            const slideWidth = slides[0].offsetWidth;
            slider.style.transform = `translateX(-${slideWidth * currentIndex}px)`;
        };

        const goToNext = () => {
            currentIndex = (currentIndex + 1) % slides.length;
            updateSlider();
        };

        const goToPrev = () => {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            updateSlider();
        };

        // Event Listeners
        nextBtn.addEventListener('click', goToNext);
        prevBtn.addEventListener('click', goToPrev);

        // Responsive handling
        window.addEventListener('resize', updateSlider);

        // Auto-slide functionality (optional)
        // setInterval(goToNext, 5000); // Auto-slide every 5 seconds
        
        // Initial setup
        updateSlider();
    }


    // --- 5. Admission Form Submission Handling (Optional) ---
    // If Flask/Jinja is handling the submission, this is optional,
    // but useful for client-side feedback.
    const admissionForm = document.getElementById("admissionForm");
    const formSuccess = document.getElementById("formSuccess");
    const formError = document.getElementById("formError");

    if (admissionForm) {
        admissionForm.addEventListener("submit", function(e) {
            // Assuming Flask will handle the actual submission and redirect on success.
            // This is just to show client-side validation/loading state.
            // If you want full AJAX submission:
            /*
            e.preventDefault();
            const formData = new FormData(admissionForm);
            fetch(admissionForm.action, { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        admissionForm.reset();
                        if (formSuccess) formSuccess.classList.remove('hidden');
                        if (formError) formError.classList.add('hidden');
                    } else {
                        if (formError) {
                            formError.textContent = data.message || "An error occurred during submission.";
                            formError.classList.remove('hidden');
                        }
                        if (formSuccess) formSuccess.classList.add('hidden');
                    }
                })
                .catch(error => {
                    console.error('Submission error:', error);
                    if (formError) {
                        formError.textContent = "Network error or server issue. Please try again.";
                        formError.classList.remove('hidden');
                    }
                    if (formSuccess) formSuccess.classList.add('hidden');
                });
            */
        });
    }

});
