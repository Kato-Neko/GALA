{% extends 'base.html' %}

{% block content %}
<div class="flex justify-center items-center min-h-screen bg-gray-100"
    style="background: linear-gradient(to bottom, #287dec, #e5d3be);">

    <form method="POST" enctype="multipart/form-data" id="update-account-form">
        {% csrf_token %}
        <div class="grid grid-cols-6 gap-4">

            <div class="col-span-1">
            </div>

            <div class="flex justify-center items-center col-span-2">
                <div class="p-2 border-4 border-dashed flex items-center justify-center w-full h-full">
                    <label for="id_image"
                        class="event-picture cursor-pointer flex flex-col items-center justify-center">
                        <div class="relative">
                            <!-- Image Preview -->
                            <img id="imagePreview"
                                src="{% if reminder.image %}{{ reminder.image.url }}{% else %}# {% endif %}"
                                alt="Preview"
                                class="object-cover rounded-lg w-[500px] h-auto max-h-[700px] {% if not reminder.image %}hidden{% endif %}">

                            <!-- Placeholder (shown when no image is selected) -->
                            {% if not reminder.image %}
                            <div id="placeholder" class="flex flex-col items-center">
                                <p class="text-white text-center">Click to upload an image</p>
                                <div
                                    class="mt-2 w-[100px] h-[100px] bg-gray-200 rounded-full flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="2" stroke="gray" class="w-8 h-8">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M12 16.5v-9m-4.5 4.5h9M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" />
                                    </svg>
                                </div>
                            </div>
                            {% endif %}
                        </div>
                    </label>
                    <input type="file" name="image" id="id_image" class="hidden" onchange="previewImage(event)">
                </div>
            </div>

            <div class="w-full border-2 rounded-lg p-6 col-span-2 flex justify-center items-center 
                bg-[rgba(173,250,217,0.2)] dark:bg-[rgba(3,2,84,0.4)]">
                <div class="w-full max-w-lg">
                    <div class="lobster-two-bold text-5xl flex justify-center text-gray-800 dark:text-white pt-3 pb-1">
                        Update Reminder
                    </div>

                    <div class="mb-4 p-4 text-red-700 dark:text-red-300 rounded-md">
                        <ul>
                            {% for field, errors in form.errors.items %}
                            <li>
                                <strong>{{ form.field.label|default:field|capfirst }}:</strong>
                                {% for error in errors %}
                                <p>{{ error }}</p>
                                {% endfor %}
                            </li>
                            {% endfor %}
                        </ul>
                    </div>


                    <div class="flex mt-2">
                        <input type="text" name="description" id="id_description" value="{{ form.description.value }}"
                            class="rounded-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Reminder Name">
                    </div>

                    <div class="flex justify-between mt-2 text-white rounded-lg">
                        <div class="flex pr-1 w-1/2">
                            <span
                                class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-e-0 border-gray-300 rounded-s-md dark:bg-gray-600 dark:text-gray-400 dark:border-gray-600">
                                <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                    viewBox="0 0 24 24">
                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                        stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                                </svg>
                            </span>
                            <input type="time" name="start_time" id="id_start_time"
                                value="{{ form.start_time.value|time:'H:i' }}"
                                class="rounded-none rounded-e-rg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Start Time">
                        </div>

                        <div class="flex pl-1 w-1/2">
                            <input type="time" name="end_time" id="id_end_time"
                                value="{{ form.end_time.value|time:'H:i' }}"
                                class="rounded-none rounded-e-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="End Time">
                        </div>
                    </div>

                    <div class="flex mt-2">
                        <span
                            class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-e-0 border-gray-300 rounded-s-md dark:bg-gray-600 dark:text-gray-400 dark:border-gray-600">
                            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                viewBox="0 0 24 24">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M4 10h16M8 14h8m-4-7V4M7 7V4m10 3V4M5 20h14a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1Z" />
                            </svg>
                        </span>
                        <input type="date" name="date" id="id_date" value="{{ form.date.value|date:'Y-m-d' }}"
                            class="rounded-none rounded-e-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Date">
                    </div>

                    <div class="flex justify-between mt-2 text-white rounded-lg">
                        <div class="flex pr-1 w-1/2">
                            <span
                                class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-e-0 border-gray-300 rounded-s-md dark:bg-gray-600 dark:text-gray-400 dark:border-gray-600">
                                <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                    viewBox="0 0 24 24">
                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                        stroke-width="1.5" d=" M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12
                                        21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12
                                        3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686
                                        0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959
                                        0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162
                                        0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113
                                        1.157-4.418" />
                                </svg>
                            </span>
                            <input type="text" name="longitude" id="id_longitude" value="{{ form.longitude.value }}"
                                class="rounded-none rounded-e-rg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Longitude">
                        </div>
                        <div class="flex pl-1 w-1/2">
                            <input type="text" name="latitude" id="id_latitude" value="{{ form.latitude.value }}"
                                class="rounded-none rounded-e-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Latitude">
                        </div>
                    </div>

                    <div class="flex mt-4 text-white rounded-lg gap-x-2">
                        <button type="submit"
                            class="flex-1 text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-800">
                            Update
                        </button>
                        <button type="button" onclick="window.location.href='{% url 'reminder-list' %}'"
                            class="flex-1 text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">
                            Cancel
                        </button>
                    </div>
                </div>
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