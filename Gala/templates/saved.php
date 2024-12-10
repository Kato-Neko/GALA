{% extends 'base.html' %}
{% load static %}

{% block content %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="csrf-token" content="{{ csrf_token }}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saved Posts</title>

    <script src="https://cdn.tailwindcss.com"></script>
    <script>
    tailwind.config = {
        theme: {
            extend: {
                colors: {
                    primary: '#00386d',
                    dark: '#b70000',
                    light: '#EAF4FA',
                    green: '#28a745',
                },
                backgroundImage: {
                    'gradient-dark': 'linear-gradient(to bottom right, #00386d, #005082)',
                },
            },
        },
    };
    </script>

    <link rel="stylesheet" href="{% static 'css/suggestions.css' %}">
    <link rel="stylesheet" href="{% static 'css/fonts.css' %}">
</head>


<body class="imnida" style="background: linear-gradient(to bottom, #287dec, #e5d3be); min-height: 100vh;">
    <div class="main-content relative py-10 px-4" style="padding-top: 120px;">
        <div class="text-center mb-6">
            <h1 class="text-4xl font-extrabold text-white tracking-wide drop-shadow-md">
                🎄 Saved Locations 🎁
            </h1>
        </div>
        <div class="flex flex-wrap gap-6 justify-center">
            {% for item in saved_reminders %}
            <div class="location-card p-4 bg-white shadow-md rounded-lg hover:shadow-lg transition w-80">

                <h3 class="text-xl font-bold text-green-600 mb-2">
                    {{ item.description }}
                </h3>
                <ul class="text-gray-700 text-sm space-y-1">
                    <li><strong>Date:</strong> {{ item.date }}</li>
                    <li><strong>Time:</strong> {{ item.start_time|default:"N/A" }} - {{ item.end_time|default:"N/A" }}
                    </li>
                    <li><strong>Address:</strong> {{ item.address }}</li>
                </ul>
                <div class="flex justify-end mt-4">
                    <button onclick="toggleSave({{ item.id }}, 'reminder', this)"
                        class="text-green-600 hover:text-green-800">
                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                            <path
                                d="M7.833 2c-.507 0-.98.216-1.318.576A1.92 1.92 0 0 0 6 3.89V21a1 1 0 0 0 1.625.78L12 18.28l4.375 3.5A1 1 0 0 0 18 21V3.889c0-.481-.178-.954-.515-1.313A1.808 1.808 0 0 0 16.167 2H7.833Z" />
                        </svg>
                    </button>
                </div>
            </div>
            {% endfor %}

            {% for item in saved_locations %}
            <div class="location-card p-4 bg-white shadow-md rounded-lg hover:shadow-lg transition w-80">

                <h3 class="text-xl font-bold text-red-600 mb-2">
                    {{ item.name }}
                </h3>
                <p class="text-gray-600 italic mb-4">{{ item.description }}</p>
                <ul class="text-gray-700 text-sm space-y-1">
                    <li><strong>Address:</strong> {{ item.address }}</li>
                    <li><strong>Weather:</strong> {{ item.weather }}</li>
                </ul>
                <div class="flex justify-end mt-4">
                    <button onclick="toggleSave({{ item.id }}, 'location', this)"
                        class="text-red-600 hover:text-red-800">
                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                            <path
                                d="M7.833 2c-.507 0-.98.216-1.318.576A1.92 1.92 0 0 0 6 3.89V21a1 1 0 0 0 1.625.78L12 18.28l4.375 3.5A1 1 0 0 0 18 21V3.889c0-.481-.178-.954-.515-1.313A1.808 1.808 0 0 0 16.167 2H7.833Z" />
                        </svg>
                    </button>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>

</html>
{% endblock %}