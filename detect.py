import argparse, warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO


def transformer_opt(opt):
    opt = vars(opt)
    del opt['source']
    del opt['weight']
    del opt['save_verbose']
    return opt

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weight', type=str, default='/workspace/cv-docker/joey04.li/datasets/master_thesis_yolov8/runs/train/v8s_300ep_128bs_Adam_10.20datasets/weights/best.pt', help='training model path')
    parser.add_argument('--source', type=str, default='/workspace/cv-docker/joey04.li/datasets/video_data/10.22.mp4', help='source directory for images or videos')
    parser.add_argument('--conf', type=float, default=0.25, help='object confidence threshold for detection')
    parser.add_argument('--iou', type=float, default=0.7, help='intersection over union (IoU) threshold for NMS')
    parser.add_argument('--mode', type=str, default='track', choices=['predict', 'track'], help='predict mode or track mode')
    parser.add_argument('--project', type=str, default='runs/detect', help='project name')
    parser.add_argument('--name', type=str, default='test_11_28_bytetrack_5fps', help='experiment name (project/name)')
    parser.add_argument('--show', action="store_true", help='show results if possible')
    parser.add_argument('--save_verbose', type=str, default='/workspace/cv-docker/joey04.li/datasets/master_thesis_yolov8/runs/detect/test_11_28_bytetrack_5fps/verbose.txt', help='save detail predict verbose results as .txt file')
    parser.add_argument('--save_txt', action="store_true", help='save results as .txt file')
    parser.add_argument('--save_conf', action="store_true", help='save results with confidence scores')
    parser.add_argument('--show_labels', action="store_true", default=False, help='show object labels in plots')
    parser.add_argument('--show_conf', action="store_true", default=False, help='show object confidence scores in plots')
    parser.add_argument('--vid_stride', type=int, default=5, help='video frame-rate stride')
    parser.add_argument('--line_width', type=int, default=1, help='line width of the bounding boxes')
    parser.add_argument('--visualize', action="store_true", help='visualize model features')
    parser.add_argument('--augment', action="store_true", help='apply image augmentation to prediction sources')
    parser.add_argument('--agnostic_nms', action="store_true", help='class-agnostic NMS')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--retina_masks', action="store_true", help='use high-resolution segmentation masks')
    parser.add_argument('--boxes', action="store_true", default=True, help='Show boxes in segmentation predictions')
    parser.add_argument('--save', action="store_true", default=True, help='save result')
    parser.add_argument('--tracker', type=str, default='bytetrack.yaml', choices=['botsort.yaml', 'bytetrack.yaml', 'deepocsort.yaml', 'hybirdsort.yaml', 'ocsort.yaml'], help='tracker type, [botsort.yaml, bytetrack.yaml, deepocsort.yaml, hybirdsort.yaml, ocsort.yaml]')
    parser.add_argument('--reid_weight', type=str, default='/workspace/cv-docker/joey04.li/datasets/yolo_tracking/examples/weights/osnet_x1_0_imagenet.pt', help='if tracker have reid, add reid model path')

    return parser.parse_known_args()[0]

class YOLOV8(YOLO):
    '''
    weigth:model path
    '''
    def __init__(self, weight='', task=None) -> None:
        super().__init__(weight, task)
    
if __name__ == '__main__':
    opt = parse_opt()
    
    model = YOLOV8(weight=opt.weight)
    verbose_path = opt.save_verbose
    if opt.mode == 'predict':
        model.predict(source=opt.source, verbose_path=verbose_path, **transformer_opt(opt))
    elif opt.mode == 'track':
        model.track(source=opt.source,
                    tracker=opt.tracker,
                    reid_weight=opt.reid_weight,
                    # **transformer_opt(opt),
                    conf=opt.conf,
                    iou=opt.iou,
                    show=opt.show,
                    stream=False,
                    # device=opt.device,
                    show_conf=opt.show_conf,
                    save_txt=opt.save_txt,
                    show_labels=opt.show_labels,
                    save=opt.save,
                    # verbose=opt.verbose,
                    # exist_ok=opt.exist_ok,
                    project=opt.project,
                    name=opt.name,
                    classes=opt.classes,
                    # imgsz=opt.imgsz,
                    vid_stride=opt.vid_stride,
                    line_width=opt.line_width)
