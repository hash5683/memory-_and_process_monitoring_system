import psutil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

def home(request):
    return render(request, 'home.html') 


def get_system_stats(request):
    """
    View to fetch and render system stats (CPU usage, memory) in HTML format.
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    
    stats = {
        'cpu_percent': cpu_percent,
        'memory_total': memory_info.total,
        'memory_used': memory_info.used,
        'memory_percent': memory_info.percent,
    }

    return render(request, 'system_stats.html', stats)

def get_process_list(request):
    """
    View to fetch and render the list of active processes in HTML format.
    """
    process_list = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_list.append(proc.info)
        except psutil.NoSuchProcess:
            pass  # Skip processes that terminate during iteration

    # Pass the process list to the template as context
    return render(request, 'process_list.html', {'processes': process_list})


@csrf_exempt
def kill_process(request):
    """
    API to kill a process by its PID.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pid = data.get('pid')
            if pid is not None:
                proc = psutil.Process(pid)
                proc.terminate()
                return JsonResponse({'message': f'Process {pid} terminated successfully.'})
            else:
                return JsonResponse({'error': 'PID not provided.'}, status=400)
        except psutil.NoSuchProcess:
            return JsonResponse({'error': 'Process not found.'}, status=404)
        except psutil.AccessDenied:
            return JsonResponse({'error': 'Permission denied. Could not terminate the process.'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
