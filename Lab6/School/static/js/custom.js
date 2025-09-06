// Custom JavaScript for School Management System
// No external dependencies - all functionality is self-contained

// Utility Functions
function $(selector) {
    return document.querySelector(selector);
}

function $$(selector) {
    return document.querySelectorAll(selector);
}

// DOM Ready Function
function ready(fn) {
    if (document.readyState !== 'loading') {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

// Auto-hide alerts after 5 seconds
ready(function() {
    const alerts = $$('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            fadeOut(alert, 500);
        }, 5000);
    });
});

// Fade out animation
function fadeOut(element, duration) {
    let opacity = 1;
    const timer = setInterval(function() {
        if (opacity <= 0.1) {
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = opacity;
        opacity -= opacity * 0.1;
    }, duration / 10);
}

// Fade in animation
function fadeIn(element, duration) {
    element.style.opacity = 0;
    element.style.display = 'block';
    let opacity = 0;
    const timer = setInterval(function() {
        if (opacity >= 1) {
            clearInterval(timer);
        }
        element.style.opacity = opacity;
        opacity += 0.1;
    }, duration / 10);
}

// Smooth scrolling for anchor links
ready(function() {
    const anchorLinks = $$('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = $(targetId);
            
            if (targetElement) {
                e.preventDefault();
                smoothScrollTo(targetElement.offsetTop - 100, 1000);
            }
        });
    });
});

// Smooth scroll function
function smoothScrollTo(targetY, duration) {
    const startY = window.pageYOffset;
    const distance = targetY - startY;
    let startTime = null;

    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = easeInOutQuad(timeElapsed, startY, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) requestAnimationFrame(animation);
    }

    function easeInOutQuad(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation);
}

// Form validation
ready(function() {
    const forms = $$('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Statistics cards animation
ready(function() {
    const statsCards = $$('.stats-card');
    statsCards.forEach(function(card, index) {
        setTimeout(function() {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            
            setTimeout(function() {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 200);
    });
});

// Table row hover effects
ready(function() {
    const tableRows = $$('table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(52, 152, 219, 0.1)';
            this.style.transform = 'scale(1.01)';
            this.style.transition = 'all 0.3s ease';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
            this.style.transform = 'scale(1)';
        });
    });
});

// Button hover effects
ready(function() {
    const buttons = $$('.btn');
    buttons.forEach(function(btn) {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'all 0.3s ease';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Card hover effects
ready(function() {
    const cards = $$('.card');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        });
    });
});

// Search functionality
function initializeSearch() {
    const searchInput = $('#search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const searchableItems = $$('.searchable-item');
            
            searchableItems.forEach(function(item) {
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
}

// Initialize search on page load
ready(initializeSearch);

// Modal functionality (simple implementation)
function showModal(modalId) {
    const modal = $('#' + modalId);
    if (modal) {
        modal.style.display = 'block';
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function hideModal(modalId) {
    const modal = $('#' + modalId);
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
}

// Close modal when clicking outside
ready(function() {
    const modals = $$('.modal');
    modals.forEach(function(modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideModal(modal.id);
            }
        });
    });
});

// Dropdown functionality
ready(function() {
    const dropdownToggles = $$('.dropdown-toggle');
    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('dropdown-menu')) {
                const isVisible = dropdown.style.display === 'block';
                
                // Hide all other dropdowns
                $$('.dropdown-menu').forEach(function(menu) {
                    menu.style.display = 'none';
                });
                
                // Toggle current dropdown
                dropdown.style.display = isVisible ? 'none' : 'block';
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            $$('.dropdown-menu').forEach(function(menu) {
                menu.style.display = 'none';
            });
        }
    });
});

// Navbar toggle for mobile
ready(function() {
    const navbarToggler = $('.navbar-toggler');
    const navbarCollapse = $('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            const isExpanded = navbarCollapse.classList.contains('show');
            
            if (isExpanded) {
                navbarCollapse.classList.remove('show');
                navbarCollapse.style.display = 'none';
            } else {
                navbarCollapse.classList.add('show');
                navbarCollapse.style.display = 'block';
            }
        });
    }
});

// Loading spinner
function showSpinner(containerId) {
    const container = $('#' + containerId);
    if (container) {
        container.innerHTML = '<div class="spinner"></div>';
    }
}

function hideSpinner(containerId) {
    const container = $('#' + containerId);
    if (container) {
        const spinner = container.querySelector('.spinner');
        if (spinner) {
            spinner.remove();
        }
    }
}

// Form submission with loading
ready(function() {
    const forms = $$('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = 'جاري المعالجة...';
                
                // Re-enable after 3 seconds (fallback)
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'حفظ';
                }, 3000);
            }
        });
    });
});

// Store original button text
ready(function() {
    const submitBtns = $$('button[type="submit"]');
    submitBtns.forEach(function(btn) {
        btn.setAttribute('data-original-text', btn.innerHTML);
    });
});

// Confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Delete confirmation
ready(function() {
    const deleteLinks = $$('.delete-link');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const message = this.getAttribute('data-confirm') || 'هل أنت متأكد من الحذف؟';
            const href = this.href;
            
            confirmAction(message, function() {
                window.location.href = href;
            });
        });
    });
});

// Toast notifications (simple implementation)
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} toast-notification`;
    toast.innerHTML = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(function() {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(function() {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(function() {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 5000);
}

// Export functions for global use
window.showModal = showModal;
window.hideModal = hideModal;
window.showSpinner = showSpinner;
window.hideSpinner = hideSpinner;
window.confirmAction = confirmAction;
window.showToast = showToast;
