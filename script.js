// swipekarbhai Website JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Header scroll effect
    const header = document.querySelector('.header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'var(--primary-white)';
            header.style.backdropFilter = 'none';
        }
        
        lastScrollTop = scrollTop;
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all animated elements
    const animatedElements = document.querySelectorAll('.category-item, .card-item, .news-item, .guide-item, .partner-item');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Credit card hover effects
    const creditCards = document.querySelectorAll('.card');
    creditCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = this.style.transform + ' scale(1.05)';
            this.style.zIndex = '10';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = this.style.transform.replace(' scale(1.05)', '');
            this.style.zIndex = this.classList.contains('card-blue') ? '2' : '1';
        });
    });

    // Apply Now button interactions
    const applyButtons = document.querySelectorAll('.apply-btn');
    applyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add loading state
            const originalText = this.textContent;
            this.textContent = 'Processing...';
            this.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                this.textContent = 'Redirecting...';
                setTimeout(() => {
                    // In a real application, this would redirect to the actual application page
                    alert('This would redirect to the credit card application page.');
                    this.textContent = originalText;
                    this.disabled = false;
                }, 1000);
            }, 1500);
        });
    });

    // Show More functionality for news and guides
    const showMoreButtons = document.querySelectorAll('.show-more-btn');
    showMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            const section = this.closest('section');
            const hiddenItems = section.querySelectorAll('.news-item:nth-child(n+7), .guide-item:nth-child(n+7)');
            
            if (hiddenItems.length > 0) {
                hiddenItems.forEach(item => {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, 100);
                });
                this.textContent = 'Show Less';
            } else {
                const allItems = section.querySelectorAll('.news-item, .guide-item');
                allItems.forEach((item, index) => {
                    if (index >= 6) {
                        item.style.opacity = '0';
                        item.style.transform = 'translateY(30px)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 300);
                    }
                });
                this.textContent = 'Show More';
            }
        });
    });

    // Search functionality (basic implementation)
    function createSearchBox() {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.innerHTML = `
            <input type="text" id="cardSearch" placeholder="Search credit cards..." class="search-input">
            <div id="searchResults" class="search-results"></div>
        `;
        
        const categoriesSection = document.querySelector('.categories .container');
        categoriesSection.insertBefore(searchContainer, categoriesSection.querySelector('h2'));
        
        const searchInput = document.getElementById('cardSearch');
        const searchResults = document.getElementById('searchResults');
        
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cardItems = document.querySelectorAll('.card-item');
            
            if (query.length > 2) {
                const matches = [];
                cardItems.forEach(card => {
                    const cardName = card.querySelector('h3').textContent.toLowerCase();
                    if (cardName.includes(query)) {
                        matches.push(card);
                    }
                });
                
                if (matches.length > 0) {
                    searchResults.innerHTML = matches.map(card => 
                        `<div class="search-result-item">${card.querySelector('h3').textContent}</div>`
                    ).join('');
                    searchResults.style.display = 'block';
                } else {
                    searchResults.innerHTML = '<div class="no-results">No cards found</div>';
                    searchResults.style.display = 'block';
                }
            } else {
                searchResults.style.display = 'none';
            }
        });
        
        // Hide search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchContainer.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }

    // Filter functionality for credit cards
    function createFilterButtons() {
        const filterContainer = document.createElement('div');
        filterContainer.className = 'filter-container';
        filterContainer.innerHTML = `
            <div class="filter-buttons">
                <button class="filter-btn active" data-filter="all">All Cards</button>
                <button class="filter-btn" data-filter="free">Lifetime Free</button>
                <button class="filter-btn" data-filter="rewards">Rewards</button>
                <button class="filter-btn" data-filter="cashback">Cashback</button>
                <button class="filter-btn" data-filter="travel">Travel</button>
            </div>
        `;
        
        const popularCardsSection = document.querySelector('.popular-cards .container');
        popularCardsSection.insertBefore(filterContainer, popularCardsSection.querySelector('.cards-grid'));
        
        const filterButtons = document.querySelectorAll('.filter-btn');
        const cardItems = document.querySelectorAll('.card-item');
        
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                
                cardItems.forEach(card => {
                    const cardName = card.querySelector('h3').textContent.toLowerCase();
                    let shouldShow = true;
                    
                    if (filter !== 'all') {
                        shouldShow = cardName.includes(filter) || 
                                   (filter === 'free' && card.textContent.includes('Lifetime Free')) ||
                                   (filter === 'rewards' && card.textContent.includes('Reward')) ||
                                   (filter === 'cashback' && card.textContent.includes('Cashback')) ||
                                   (filter === 'travel' && card.textContent.includes('Travel'));
                    }
                    
                    if (shouldShow) {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 100);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(30px)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }

    // Mobile menu toggle
    function createMobileMenu() {
        const header = document.querySelector('.header-content');
        const nav = document.querySelector('.nav');
        
        const menuToggle = document.createElement('button');
        menuToggle.className = 'mobile-menu-toggle';
        menuToggle.innerHTML = '☰';
        menuToggle.setAttribute('aria-label', 'Toggle navigation menu');
        
        header.insertBefore(menuToggle, nav);
        
        menuToggle.addEventListener('click', function() {
            nav.classList.toggle('nav-open');
            this.innerHTML = nav.classList.contains('nav-open') ? '✕' : '☰';
        });
        
        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-list a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                nav.classList.remove('nav-open');
                menuToggle.innerHTML = '☰';
            });
        });
    }

    // Form validation for newsletter signup (if added)
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Error handling for images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'image-placeholder';
            placeholder.textContent = 'Image not available';
            placeholder.style.cssText = `
                background: var(--light-gray);
                color: var(--text-gray);
                display: flex;
                align-items: center;
                justify-content: center;
                height: 200px;
                border-radius: 10px;
                font-weight: 500;
            `;
            this.parentNode.insertBefore(placeholder, this);
        });
    });

    // Lazy loading for better performance
    const lazyElements = document.querySelectorAll('.card-placeholder, .news-placeholder, .guide-placeholder');
    const lazyObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                lazyObserver.unobserve(entry.target);
            }
        });
    });

    lazyElements.forEach(el => {
        el.style.opacity = '0.8';
        el.style.transition = 'opacity 0.3s ease';
        lazyObserver.observe(el);
    });

    // Initialize features
    createSearchBox();
    createFilterButtons();
    createMobileMenu();

    // Add styles for new elements
    const additionalStyles = `
        <style>
        .search-container {
            margin-bottom: 2rem;
            position: relative;
            max-width: 400px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .search-input {
            width: 100%;
            padding: 12px 20px;
            border: 2px solid var(--border-color);
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s ease;
        }
        
        .search-input:focus {
            border-color: var(--primary-yellow);
        }
        
        .search-results {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--primary-white);
            border-radius: 10px;
            box-shadow: var(--shadow);
            z-index: 10;
            display: none;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .search-result-item, .no-results {
            padding: 12px 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .search-result-item:hover {
            background: var(--light-yellow);
        }
        
        .no-results {
            color: var(--text-gray);
            text-align: center;
        }
        
        .filter-container {
            margin-bottom: 2rem;
        }
        
        .filter-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            background: var(--primary-white);
            color: var(--text-dark);
            border: 2px solid var(--border-color);
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .filter-btn:hover, .filter-btn.active {
            background: var(--primary-yellow);
            border-color: var(--primary-yellow);
            color: var(--text-dark);
        }
        
        .mobile-menu-toggle {
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-dark);
        }
        
        @media (max-width: 768px) {
            .mobile-menu-toggle {
                display: block;
            }
            
            .nav {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: var(--primary-white);
                box-shadow: var(--shadow);
                transform: translateY(-100%);
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
            }
            
            .nav-open {
                transform: translateY(0);
                opacity: 1;
                visibility: visible;
            }
            
            .nav-list {
                flex-direction: column;
                padding: 1rem;
            }
            
            .filter-buttons {
                justify-content: flex-start;
                overflow-x: auto;
                padding-bottom: 10px;
            }
            
            .filter-btn {
                white-space: nowrap;
                flex-shrink: 0;
            }
        }
        </style>
    `;
    
    document.head.insertAdjacentHTML('beforeend', additionalStyles);

    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`swipekarbhai website loaded in ${loadTime}ms`);
        });
    }

    // Analytics placeholder (would integrate with actual analytics service)
    function trackEvent(category, action, label) {
        console.log(`Analytics: ${category} - ${action} - ${label}`);
        // In production, this would send data to analytics service
    }

    // Track button clicks
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('apply-btn')) {
            trackEvent('Credit Card', 'Apply Click', e.target.closest('.card-item').querySelector('h3').textContent);
        }
        if (e.target.classList.contains('filter-btn')) {
            trackEvent('Filter', 'Filter Click', e.target.textContent);
        }
    });

    console.log('swipekarbhai website initialized successfully! 🎉');
});

// Scroll to top functionality
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Service Worker registration for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        scrollToTop,
        debounce
    };
}
