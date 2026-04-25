import requests
import xml.etree.ElementTree as ET
import re

def generate_m3u():
    xml_url = 'https://only4.tv/epg/epg.xml'
    output_file = 'playlist.m3u'
    cdn_base_url = 'http://cdn.only4.online/'
    
    print(f"Đang tải dữ liệu từ: {xml_url}...")
    
    try:
        # Tải file XML (thêm headers để tránh bị server chặn)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(xml_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            count = 0
            
            # Quét tất cả thẻ <channel>
            for channel in root.findall('channel'):
                channel_id = channel.get('id')
                icon_elem = channel.find('icon')
                numeric_id = None
                icon_url = ""
                
                # Nếu có thẻ icon, tìm số nằm giữa /ch/ và .png
                if icon_elem is not None:
                    icon_url = icon_elem.get('src', '')
                    match = re.search(r'/ch/(\d+)\.png', icon_url)
                    if match:
                        numeric_id = match.group(1) # Lấy ra số, ví dụ 20106
                
                # Chỉ xử lý nếu tìm thấy số ID hợp lệ
                if numeric_id:
                    # Lấy tên kênh
                    display_name_elem = channel.find('display-name')
                    channel_name = display_name_elem.text if display_name_elem is not None else channel_id
                    
                    # Tạo cấu trúc URL chuẩn: http://cdn.only4.online/20106/index.m3u8?token=
                    stream_url = f"{cdn_base_url}{numeric_id}/index.m3u8?token="
                    
                    # Ghi định dạng M3U (thêm luôn logo vào cho đẹp)
                    logo_attr = f' tvg-logo="{icon_url}"' if icon_url else ""
                    f.write(f'#EXTINF:-1 tvg-id="{channel_id}"{logo_attr},{channel_name}\n')
                    f.write(f'{stream_url}\n')
                    count += 1
            
            print(f"✅ Thành công! Đã tạo playlist với {count} kênh.")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    generate_m3u()
