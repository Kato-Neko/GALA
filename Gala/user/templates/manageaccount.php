{% extends 'base.html' %}
{% load static %}

{% block title %}
GALA - Account Management
{% endblock %}

<head>
    <link rel="stylesheet" href="{% static 'css/fonts.css' %}">
</head>

{% block content %}
<div class="h-screen flex items-center justify-center"
    style="background: linear-gradient(to bottom, #287dec, #e5d3be);">
    <form id="update-account-form" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="grid grid-cols-6 gap-4">

            <div class="col-span-1">
            </div>

            <!-- First column: Avatar with fixed width -->
            <div class="flex justify-center items-center col-span-2">
                <div class="p-2 border-4 border-dashed flex items-center justify-center w-full h-full">
                    <label for="profile_picture"
                        class="event-picture cursor-pointer flex flex-col items-center justify-center">
                        <div class="relative">
                            <!-- Image Preview -->
                            <img id="imagePreview"
                                src="{% if user.profile.profile_picture %}{{ user.profile.profile_picture.url }}{% else %}# {% endif %}"
                                alt="Profile Picture Preview"
                                class="object-cover rounded-lg w-[500px] h-auto max-h-[700px] {% if not user.profile.profile_picture %}hidden{% endif %}">

                            <!-- Placeholder (shown when no image is selected) -->
                            {% if not user.profile.profile_picture %}
                            <div id="placeholder" class="flex flex-col items-center">
                                <p class="text-white text-center">Click to upload an image</p>
                                <div
                                    class="mt-2 w-[100px] h-[100px] bg-gray-200 rounded-full flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="gray" class="w-8 h-8">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M12 16.5v-9m-4.5 4.5h9M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" />
                                    </svg>
                                </div>
                            </div>
                            {% endif %}
                        </div>
                    </label>
                    <input type="file" name="profile_picture" id="profile_picture" class="hidden"
                        onchange="previewImage(event)">
                </div>
            </div>

            <!-- Second column: Form content -->
            <div class="w-full border-2 rounded-lg p-6 col-span-2 flex justify-center items-center"
                style="background: rgba(3, 2, 84, 0.4);">
                <div class="w-full max-w-lg">
                    <!-- Email Address -->
                    <div class="relative mb-4">
                        <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
                            <svg class="w-5 h-5 text-gray-800 dark:text-white" aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                                viewBox="0 0 24 24">
                                <path
                                    d="M2.038 5.61A2.01 2.01 0 0 0 2 6v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6c0-.12-.01-.238-.03-.352l-.866.65-7.89 6.032a2 2 0 0 1-2.429 0L2.884 6.288l-.846-.677Z" />
                                <path
                                    d="M20.677 4.117A1.996 1.996 0 0 0 20 4H4c-.225 0-.44.037-.642.105l.758.607L12 10.742 19.9 4.7l.777-.583Z" />
                            </svg>
                        </div>
                        <input type="text" id="email" name="email"
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Email Address" value="{{ user.email }}">
                    </div>

                    <!-- Full Name -->
                    <div class="relative flex mb-4">
                        <div class="w-1/2 pr-2">
                            <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
                                <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                                    viewBox="0 0 24 24">
                                    <path fill-rule="evenodd"
                                        d="M12 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm-2 9a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-1a4 4 0 0 0-4-4h-4Z"
                                        clip-rule="evenodd" />
                                </svg>
                            </div>
                            <input type="text" id="first_name" name="first_name"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="First Name" value="{{ user.first_name }}">
                        </div>

                        <div class="w-1/2 pl-1">
                            <input type="text" id="last_name" name="last_name"
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-5 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Last Name" value="{{ user.last_name }}">
                        </div>
                    </div>

                    <!-- Username -->
                    <div class="relative mb-4">
                        <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
                            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                                viewBox="0 0 24 24">
                                <path fill-rule="evenodd"
                                    d="M5 8a4 4 0 1 1 7.796 1.263l-2.533 2.534A4 4 0 0 1 5 8Zm4.06 5H7a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h2.172a2.999 2.999 0 0 1-.114-1.588l.674-3.372a3 3 0 0 1 .82-1.533L9.06 13Zm9.032-5a2.907 2.907 0 0 0-2.056.852L9.967 14.92a1 1 0 0 0-.273.51l-.675 3.373a1 1 0 0 0 1.177 1.177l3.372-.675a1 1 0 0 0 .511-.273l6.07-6.07a2.91 2.91 0 0 0-.944-4.742A2.907 2.907 0 0 0 18.092 8Z"
                                    clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input type="text" id="update-username" name="username"
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Username" value="{{ user.username }}">
                    </div>

                    <!-- Password -->
                    <div class="relative mb-4">
                        <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
                            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                                viewBox="0 0 24 24">
                                <path fill-rule="evenodd"
                                    d="M5 8a4 4 0 1 1 7.796 1.263l-2.533 2.534A4 4 0 0 1 5 8Zm4.06 5H7a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h2.172a2.999 2.999 0 0 1-.114-1.588l.674-3.372a3 3 0 0 1 .82-1.533L9.06 13Zm9.032-5a2.907 2.907 0 0 0-2.056.852L9.967 14.92a1 1 0 0 0-.273.51l-.675 3.373a1 1 0 0 0 1.177 1.177l3.372-.675a1 1 0 0 0 .511-.273l6.07-6.07a2.91 2.91 0 0 0-.944-4.742A2.907 2.907 0 0 0 18.092 8Z"
                                    clip-rule="evenodd" />
                            </svg>
                        </div>
                        <input type="text" id="update-password" name="password"
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Password">
                    </div>

                    <div class="relative mb-4 flex flex-col gap-2">
                        <button type="button" onclick="openUpdateModal()"
                            class="w-full text-white border-white hover:text-white border hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-800">
                            Update Account</button>
                        <button type="button" onclick="openDeleteModal()"
                            class="w-full text-white border-white hover:text-white border hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">
                            Delete Account</button>
                    </div>
                </div>
            </div>
        </div>


        <!-- Delete Confirmation Modal -->
        <div id="deleteModal"
            class="hidden fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 backdrop-blur-md z-[9999]">
            <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full text-center">
                <h2 class="text-xl font-bold text-gray-800 mb-4">Confirm Account Deletion</h2>
                <p class="text-sm text-gray-600 mb-6">This action cannot be undone. Are you sure you want to delete your
                    account?</p>
                <button type="submit" onclick="closeDeleteModal()"
                    class="w-full text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-800">
                    Cancel</button>
                <form method="post" action="{% url 'delete_account' %}">
                    {% csrf_token %}
                    <button type="submit"
                        class="w-full text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">
                        Confirm</button>
                </form>
            </div>
        </div>

        <!-- Update Confirmation Modal -->
        <div id="updateModal"
            class="hidden fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 backdrop-blur-md z-[9999]">
            <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full text-center">
                <h2 class="text-xl font-bold text-gray-800 mb-4">Confirm Account Update</h2>
                <p class="text-sm text-gray-600 mb-6">Are you sure you want to update your account information?</p>
                <button type="button" onclick="closeUpdateModal()"
                    class="w-full text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">Cancel</button>
                <button type="button" onclick="confirmUpdate()"
                    class="w-full text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-800">
                    Confirm</button>
            </div>
        </div>
    </form>
</div>


<script>
function previewImage(event) {
    const fileInput = event.target;
    const preview = document.getElementById('imagePreview');
    const placeholder = document.getElementById('placeholder');

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('hidden'); // Show the image preview
            placeholder?.classList.add('hidden'); // Hide the placeholder
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
}
</script>
{% endblock %}