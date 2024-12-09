{% extends 'base.html' %}

{% block content %}
<div class="w-screen h-screen pt-10"
    style="background: linear-gradient(to bottom, rgb(8, 68, 146), rgb(229, 211, 190));">
    <div class="grid grid-cols-7 gap-4 pt-20">
        <div class="col-span-1"></div>

        <!-- Scrollable List Container -->
        <div class="center-rectangle col-span-2 shadow-xl p-10 mt-5 rounded-2xl max-w-xl h-[700px] w-full relative"
            style="background: rgba(3, 2, 84, 0.4);">
            <!-- Scrollable Event List -->
            <div class="relative mt-4 space-y-6 h-full overflow-y-auto no-scrollbar z-10">
                {% for reminder in reminders %}
                <div class="event-item group relative p-4 rounded-2xl text-white"
                    style="background-color: {{ reminder.color }};">
                    {% if reminder.image %}
                    <img src="{{ reminder.image }}" alt="{{ reminder.title }}"
                        class="w-full h-32 object-cover rounded-lg mb-4">
                    {% endif %}
                    <h4 class="font-bold text-lg">{{ reminder.title }}</h4>
                    <p>{{ reminder.address }}</p>
                    <p>Distance: {{ reminder.distance }}</p>
                    {% if reminder.is_happening %}
                    <p class="text-white font-bold">Happening Now</p>
                    {% elif reminder.is_overdue %}
                    <p class="text-white font-bold">Missed</p>
                    {% else %}
                    <p>Time Remaining: {{ reminder.time_remaining }}</p>
                    {% endif %}
                </div>
                {% empty %}
                <p class="text-center text-gray-300">No reminders found.</p>
                {% endfor %}
            </div>
        </div>

        <!-- Calendar -->
        <div id="calendar-container"
            class="col-span-3 shadow-xl mt-5 p-5 rounded-2xl pb-7 flex justify-center items-center w-auto h-[700px] overflow-hidden"
            style="background: rgba(3, 2, 84, 0.4); color:rgba(255, 255, 255, 1);">
            <div id="calendar"></div>
        </div>
    </div>
</div>

<!-- Create Reminder Modal -->
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden" id="reminder-modal">
    <div
        class="bg-[rgba(229,211,190,0.8)] dark:bg-[rgba(0,72,166,0.8)] dark:text-white p-6 rounded-lg shadow-lg max-w-2xl w-full">
        <form method="post" action="{% url 'reminder-create' %}" id="reminder-form" enctype="multipart/form-data">
            {% csrf_token %}
            <div class="grid grid-cols-6 gap-4">

                <!-- Image Section -->
                <div class="flex justify-center items-center col-span-2">
                    <div class="p-2 border-4 border-dashed flex items-center justify-center w-full h-full">
                        <label for="id_image" class="cursor-pointer flex flex-col items-center justify-center">
                            <div class="relative">
                                <!-- Image Preview -->
                                <img id="imagePreview" src="#" alt="Preview"
                                    class="object-cover rounded-lg w-[500px] h-auto max-h-[700px] hidden">
                                <!-- Placeholder -->
                                <div id="placeholder" class="flex flex-col items-center">
                                    <p class="text-gray-700 dark:text-white text-center">Click to upload an image</p>
                                    <div
                                        class="mt-2 w-[100px] h-[100px] bg-gray-200 dark:bg-gray-600 rounded-full flex items-center justify-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                            stroke-width="2" stroke="gray" class="w-8 h-8">
                                            <path stroke-linecap="round" stroke-linejoin="round"
                                                d="M12 16.5v-9m-4.5 4.5h9M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" />
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </label>
                        <input type="file" name="image" id="id_image" class="hidden" onchange="previewImage(event)">
                    </div>
                </div>

                <!-- Form Section -->
                <div
                    class="w-full border-2 rounded-lg p-6 col-span-4 bg-[rgba(173,250,217,0.2)] dark:bg-[rgba(3,2,84,0.4)]">
                    <h2 class="lobster-two-bold text-3xl text-center text-gray-800 dark:text-white pb-4">Create Reminder
                    </h2>

                    <div class="flex mt-2">
                        <input type="text" name="description" id="id_description" placeholder="Reminder Name" required
                            class="rounded-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
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
                            <input type="time" name="start_time" id="id_start_time" required
                                class="rounded-none rounded-e-rg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Start Time">
                        </div>

                        <div class="flex pl-1 w-1/2">
                            <input type="time" name="end_time" id="id_end_time" required
                                class="rounded-none rounded-e-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="End Time">
                        </div>
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
                            <input type="text" name="longitude" id="id_longitude" required
                                class="rounded-none rounded-e-rg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Longitude">
                        </div>
                        <div class="flex pl-1 w-1/2">
                            <input type="text" name="latitude" id="id_latitude" required
                                class="rounded-none rounded-e-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Latitude">
                        </div>
                    </div>

                    <input type="hidden" name="date" id="selected-date">

                    <div class="flex mt-4 gap-x-2">
                        <button type="submit"
                            class="flex-1 bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg">Create</button>
                        <button type="button" onclick="closeCreateModal()"
                            class="flex-1 bg-gray-500 hover:bg-gray-600 text-white py-2 px-4 rounded-lg">Cancel</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>

<!-- View Reminder Modal -->
{% for reminder in reminders %}
<div class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 hidden"
    id="view-reminder-modal-{{ reminder.id }}">
    <div class=" dark:text-white p-6 rounded-lg shadow-lg max-w-8xl w-full">
        <div class="grid grid-cols-6 gap-4">

            <div class="col-span-1">
            </div>

            <!-- Image Section -->
            <div class="flex justify-center items-center col-span-2">
                <div class="p-2 border-4 border-dashed flex items-center justify-center w-full h-full">
                    <div class="relative">
                        {% if reminder.image %}
                        <img src="{{ reminder.image }}" alt="{{ reminder.description }}"
                            class="rounded-lg w-auto h-auto max-w-full max-h-full">
                        {% else %}
                        <p class="text-gray-400">No Image Available</p>
                        {% endif %}
                    </div>
                </div>
            </div>

            <div class="w-full border-2 rounded-lg p-6 col-span-2 flex justify-center items-center 
                            bg-[rgba(173,250,217,0.2)] dark:bg-[rgba(3,2,84,0.4)]">
                <div class="w-full max-w-lg">
                    <div class="flex mt-2">
                        <input type="text" name="description" id="id_description" value="{{ reminder.title }}"
                            class="rounded-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Reminder Name" disabled>
                    </div>

                    <div class="flex mt-2">
                        <span
                            class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-e-0 border-gray-300 rounded-s-md dark:bg-gray-600 dark:text-gray-400 dark:border-gray-600">
                            <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"
                                viewBox="0 0 24 24">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                    stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>
                        </span>
                        <input type="text" name="start_time" id="id_start_time"
                            value="{{ reminder.start }} - {{ reminder.end }}"
                            class="rounded-none rounded-e-rg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Start Time" disabled>
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
                        <input type="date" name="date" id="id_date" value="{{ reminder.date }}"
                            class="rounded-none rounded-e-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            placeholder="Date" disabled>
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
                            <input type="text" name="longitude" id="id_longitude" value="{{ reminder.longitude }}"
                                class="rounded-none rounded-e-rg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Longitude" disabled>
                        </div>
                        <div class="flex pl-1 w-1/2">
                            <input type="text" name="latitude" id="id_latitude" value="{{ reminder.latitude }}"
                                class="rounded-none rounded-e-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Latitude" disabled>
                        </div>
                    </div>

                    <div class="flex mt-4 gap-x-2">
                        <a href="{% url 'reminder-update' reminder.id %}"
                            class="flex-1 text-yellow-700 hover:text-white border border-yellow-700 hover:bg-yellow-800 focus:ring-4 focus:outline-none focus:ring-yellow-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-yellow-500 dark:text-yellow-500 dark:hover:text-white dark:hover:bg-yellow-600 dark:focus:ring-yellow-800">
                            Edit
                        </a>
                        <a href="{% url 'reminder-delete' reminder.id %}"
                            class="flex-1 text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">
                            Delete
                        </a>
                    </div>
                    <button type="button" onclick="closeViewModal({{ reminder.id }})"
                        class="w-full flex-1 mt-4 text-black hover:text-white border border-black hover:bg-black focus:ring-4 focus:outline-none focus:ring-black font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-white dark:text-white dark:hover:text-black dark:hover:bg-white dark:focus:ring-white">
                        Close
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>
{% endfor %}

<script>
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: {{ events | safe }},
        dayClick: function (date, jsEvent, view) {
            const today = moment().startOf('day');
            if (date.isBefore(today)) {
                alert("You cannot create a reminder for a past date.");
                return;
            }
            openCreateModal(date.format()); // Pass the selected date to the modal
        },
        eventClick: function (event, jsEvent, view) {
            // Open the view reminder modal
            openViewModal(event.id);
        }
});


    function openCreateModal(date) {
        // Set the selected date in the modal
        document.getElementById('selected-date').value = date;
        // Show the modal
        document.getElementById('reminder-modal').classList.remove('hidden');
    }

    function closeCreateModal() {
        // Hide the create modal
        document.getElementById('reminder-modal').classList.add('hidden');
    }

    function openViewModal(reminderId) {
        // Locate the specific modal for the clicked reminder and show it
        document.getElementById(`view-reminder-modal-${reminderId}`).classList.remove('hidden');
    }

    function closeViewModal(reminderId) {
        // Hide the specific view reminder modal
        document.getElementById(`view-reminder-modal-${reminderId}`).classList.add('hidden');
    }

    function previewImage(event) {
        const fileInput = event.target;
        const preview = document.getElementById('imagePreview');
        const placeholder = document.getElementById('placeholder');

        if (fileInput.files && fileInput.files[0]) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.classList.remove('hidden');
                placeholder.classList.add('hidden');
            };
            reader.readAsDataURL(fileInput.files[0]);
        }
    }

</script>

<style>
    .no-scrollbar::-webkit-scrollbar {
        display: none;
    }

    .no-scrollbar {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
</style>
{% endblock %}