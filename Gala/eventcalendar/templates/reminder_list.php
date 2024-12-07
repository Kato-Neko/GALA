{% extends 'base.html' %}

{% block content %}
<div class="w-screen h-screen pt-10" style="background: linear-gradient(to bottom, #287dec, #e5d3be);">
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
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-sm w-full">
        <h2 class="text-xl font-bold mb-4">Create Reminder</h2>
        <form method="post" action="{% url 'reminder-create' %}" id="reminder-form" enctype="multipart/form-data">
            {% csrf_token %}
            <label for="description" class="block text-sm font-medium mb-2">Description:</label>
            <input type="text" name="description" required class="w-full p-2 mb-4 border rounded-md">
            <label for="start_time" class="block text-sm font-medium mb-2">Start Time:</label>
            <input type="time" name="start_time" required class="w-full p-2 mb-4 border rounded-md">
            <label for="end_time" class="block text-sm font-medium mb-2">End Time:</label>
            <input type="time" name="end_time" required class="w-full p-2 mb-4 border rounded-md">
            <label for="longitude" class="block text-sm font-medium mb-2">Longitude:</label>
            <input type="text" name="longitude" class="w-full p-2 mb-4 border rounded-md">
            <label for="latitude" class="block text-sm font-medium mb-2">Latitude:</label>
            <input type="text" name="latitude" class="w-full p-2 mb-4 border rounded-md">
            <label for="image" class="block text-sm font-medium mb-2">Upload Image:</label>
            <input type="file" name="image" class="w-full p-2 mb-4 border rounded-md">
            <input type="hidden" name="date" id="selected-date">
            <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-700">Save</button>
        </form>
        <button class="w-full mt-4 bg-red-500 text-white py-2 rounded-md hover:bg-red-700"
            onclick="closeCreateModal()">Close</button>
    </div>
</div>

<!-- View Reminder Modal -->
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 hidden" id="view-reminder-modal">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-sm w-full">
        <h2 class="text-xl font-bold mb-4">Reminder Details</h2>
        <div id="reminder-details"></div>
        <div class="flex justify-between mt-4">
            <a id="edit-reminder-link"
                class="px-4 py-2 bg-yellow-500 text-white rounded-md hover:bg-yellow-700">Edit</a>
            <a id="delete-reminder-link" class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-700">Delete</a>
        </div>
        <button class="w-full mt-4 bg-gray-500 text-white py-2 rounded-md hover:bg-gray-700"
            onclick="closeViewModal()">Close</button>
    </div>
</div>

<script>
    $(document).ready(function () {
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
            openCreateModal(date.format());
        },
        eventClick: function (event, jsEvent, view) {
            openViewModal(event);
        }
        });
    });

    function openCreateModal(date) {
        document.getElementById('selected-date').value = date;
        document.getElementById('reminder-modal').classList.remove('hidden');
    }

    function closeCreateModal() {
        document.getElementById('reminder-modal').classList.add('hidden');
    }

    function openViewModal(event) {
        const reminderDetails = document.getElementById('reminder-details');
        const endTime = event.end ? moment(event.end).format('HH:mm') : 'No end time set';
        const longitude = event.longitude || 'Not provided';
        const latitude = event.latitude || 'Not provided';

        reminderDetails.innerHTML = `
            <p><strong>Description:</strong> ${event.title}</p>
            <p><strong>Date:</strong> ${moment(event.start).format('YYYY-MM-DD')}</p>
            <p><strong>Time:</strong> ${moment(event.start).format('HH:mm')} - ${endTime}</p>
            <p><strong>Location:</strong> Latitude ${latitude}, Longitude ${longitude}</p>
        `;

        document.getElementById('edit-reminder-link').href = `update/${event.id}`;
        document.getElementById('delete-reminder-link').href = `delete/${event.id}`;
        document.getElementById('view-reminder-modal').classList.remove('hidden');
    }

    function closeViewModal() {
        document.getElementById('view-reminder-modal').classList.add('hidden');
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