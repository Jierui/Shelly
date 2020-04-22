extern "C" {
#include <libavcodec/avcodec.h>
// #include <libavdevice/avdevice.h>
#include <libavformat/avformat.h>
// #include <libavutil/mathematics.h>
// #include <libavutil/opt.h>
// #include <libavutil/time.h>
// #include <libavutil/timestamp.h>
#include <libswscale/swscale.h>
#include <stdio.h>
}
#include <opencv2/highgui.hpp>
#include <iostream>
using namespace std;
using namespace cv;

int main(int argc, char* argv[]) {
      //nginx-rtmp 直播服务器rtmp推流URL
    const char *outUrl = "rtmp://localhost:1985/live/Cam";

    //注册所有的编解码器
    avcodec_register_all();

    //注册所有的封装器
    av_register_all();

    //注册所有网络协议
    avformat_network_init();

    Mat orgFrame;

    //像素格式转换上下文
    SwsContext *vsc = NULL;

    //输出的数据结构
    AVFrame *yuv = NULL;

    //编码器上下文
    AVCodecContext *avctx = NULL;

    //rtmp flv 封装器
    AVFormatContext *ofmt_ctx = NULL;

    VideoCapture cap("/home/loujie/study/video_deal/data/40.mp4");
    if (!cap.isOpened()) {
        cout << "error" << endl;
        return -2;
    }
    VideoCapture *m_cap = &cap;

//     if(m_cap) //VideoCapture* m_cap;
//     {
//         if(m_cap->isOpened() == false)
//         {
//             bool ret = m_cap->open("./data/40.mp4");

//             // if(ret == false && QFile::exists(DEFAULT_CAMERA_DEV))
//             // {
//             //     ret = m_cap->open(DEFAULT_CAMERA_DEV);
//             // }
//             if (!ret) {
//                 cout << "error" << endl;
//                 return -1;
//             }

// //            if(ret)
//             //            {
//             //                m_cap->set(CV_CAP_PROP_FRAME_WIDTH, 640);
//             //                m_cap->set(CV_CAP_PROP_FRAME_HEIGHT, 480);
//             //                m_cap->set(CV_CAP_PROP_FPS, 30);
//             //            }
//         }
//     }
    // else
    //     return -1;

    
    int framecnt = 0;

    int inWidth = m_cap->get(CAP_PROP_FRAME_WIDTH);
    int inHeight = m_cap->get(CAP_PROP_FRAME_HEIGHT);
    int fps = m_cap->get(CAP_PROP_FPS);

    cout << "m_cap info" << inWidth << inHeight << fps << endl;

    fps = 25;

    ///2 初始化格式转换上下文
    vsc = sws_getCachedContext(vsc,
                               inWidth, inHeight, AV_PIX_FMT_BGR24,     //、高、像素格式
                               inWidth, inHeight, AV_PIX_FMT_YUV420P,//目标宽、高、像素格式
                               SWS_BICUBIC,  // 尺寸变化使用算法
                               0, 0, 0
                               );
    if (!vsc)
    {
        return -2;
    }

    ///3 初始化输出的数据结构
    yuv = av_frame_alloc();
    yuv->format = AV_PIX_FMT_YUV420P;
    yuv->width = inWidth;
    yuv->height = inHeight;
    yuv->pts = 0;
    //分配yuv空间
    int ret = av_frame_get_buffer(yuv, 32);
    if (ret != 0)
    {
        printf("av_frame_get_buffer fail\n");
        return -3;
    }

    ///4 初始化编码上下文
    //a 找到编码器
    AVCodec *codec = avcodec_find_encoder(AV_CODEC_ID_H264);
    if (!codec)
    {
        printf("Can`t find h264 encoder!\n");
        return -13;
    }
    //b 创建编码器上下文
    avctx = avcodec_alloc_context3(codec);
    if (!avctx)
    {
        printf("avcodec_alloc_context3 failed!\n");
        return -8;
    }

    cout << "init avctx--------------------" << endl;


    //c 配置编码器参数
    avctx->codec_id = codec->id;
    avctx->thread_count = 8;

//    avctx->flags |= AV_CODEC_FLAG_GLOBAL_HEADER;

    AVDictionary *param = 0;
    av_dict_set(&param, "preset", "superfast", 0);  //编码形式修改
    av_dict_set(&param, "tune", "zerolatency", 0);  //实时编码

    avctx->width = inWidth;
    avctx->height = inHeight;


//    avctx->bit_rate = 400000;
    avctx->bit_rate = 50 * 1024 * 8;

    avctx->time_base.num = 1;
    avctx->time_base.den = fps;

    avctx->framerate.num = fps;
    avctx->framerate.den = 1;

    avctx->qmin = 10;   //调节清晰度和编码速度 //这个值调节编码后输出数据量越大输出数据量越小，越大编码速度越快，清晰度越差
    avctx->qmax = 51;

    //画面组的大小，多少帧一个关键帧
    avctx->gop_size = 50;   //编码一旦有gopsize很大的时候或者用了opencodec，有些播放器会等待I帧，无形中增加延迟。
    avctx->max_b_frames = 0;    //编码时如果有B帧会再解码时缓存很多帧数据才能解B帧，因此只留下I帧和P帧。
    avctx->pix_fmt = AV_PIX_FMT_YUV420P;

    //d 打开编码器上下文
    ret = avcodec_open2(avctx, codec, &param);
    if (ret != 0)
    {
        cout << "avcodec_open2 fail" << endl;
        return -5;
    }

    cout << "avcodec_open2 success! --------------------" << endl;

    ///5 输出封装器和视频流配置
    //a 创建输出封装器上下文
//    ret = avformat_alloc_output_context2(&ofmt_ctx, 0, "flv", outUrl);
    ret = avformat_alloc_output_context2(&ofmt_ctx, 0, "flv", NULL);  //++Huey
    if (ret != 0)
    {
        printf ("avformat_alloc_output_context2 fail\n");

        return -6;
    }

    // << "avformat_new_stream --------------------";

    //b 添加视频流
    AVStream *out_stream = avformat_new_stream(ofmt_ctx, NULL);
    if (!out_stream)
    {
        cout << "avformat_new_stream failed" <<endl;
        return -7;
    }
//    vs->codecpar->codec_tag = 0;
    out_stream->codec->codec_tag = 0;   //++Huey
    //从编码器复制参数
    cout << "avcodec_copy_context --------------------" << endl;
//    avcodec_parameters_from_context(vs->codecpar, vc);
     //++Huey
    avcodec_copy_context(out_stream->codec,avctx);

    out_stream->time_base.num = 1;
    out_stream->time_base.den = fps;

    //End++
    av_dump_format(ofmt_ctx, 0, outUrl, 1);

    // qDebug() << "avio_open --------------------";
    ///打开rtmp 的网络输出IO
    ret = avio_open(&ofmt_ctx->pb, outUrl, AVIO_FLAG_WRITE);
    if (ret != 0)
    {
        cout << "avio_open fail" << endl;

        return -9;
    }

    cout << "avformat_write_header --------------------" << endl;
    //写入封装头
    ret = avformat_write_header(ofmt_ctx, NULL);
    if (ret != 0)
    {
        cout << "avformat_write_header fail" << endl;

        return -10;
    }

    // qDebug() << "run CamPush --------------------";
    AVPacket pkt;
    av_init_packet(&pkt);
    int vpts = 0;

    while(1)
    {
        // ERROR_INFO "m_cap->grab --------------------";
        ///读取rtsp视频帧，解码视频帧
        if (!m_cap->grab())
        {
            continue;
        }

        // ERROR_INFO "m_cap->retrieve --------------------";
        ///yuv转换为rgb
        if (!m_cap->retrieve(orgFrame))
        {
            continue;
        }
        // imshow("video", orgFrame);
        // waitKey(20);


        // ERROR_INFO "rgb to yuv --------------------";
        ///rgb to yuv
        //输入的数据结构
        uint8_t *indata[AV_NUM_DATA_POINTERS] = { 0 };
        //indata[0] bgrbgrbgr
        //plane indata[0] bbbbb indata[1]ggggg indata[2]rrrrr
        indata[0] = orgFrame.data;
        int insize[AV_NUM_DATA_POINTERS] = { 0 };
        //一行（宽）数据的字节数
        insize[0] = orgFrame.cols * orgFrame.elemSize();
        int h = sws_scale(vsc, indata, insize, 0, orgFrame.rows, //源数据
                          yuv->data, yuv->linesize);
        if (h <= 0)
        {
            continue;
        }

        // ERROR_INFO "AVFrame to AVPacket --------------------";
        ///h264编码
        yuv->pts = vpts;
        vpts++;

        int got_packet = 0;

        av_init_packet(&pkt);
        if (avctx->codec_type == AVMEDIA_TYPE_VIDEO)
            ret = avcodec_encode_video2(avctx, &pkt,yuv, &got_packet);

        // qDebug() << "AVPacket Bef --"
        //          << pkt.size << pkt.pts << pkt.dts << pkt.duration
        //          << (pkt.data == NULL) << (pkt.buf == NULL);

        if(got_packet == 0 || ret != 0)
        {
            // qDebug() << "avcodec_encode_video2 fail -------------";
            continue;
        }

        //推流
        pkt.pts = av_rescale_q(pkt.pts, avctx->time_base, out_stream->time_base);
//        pkt.dts = av_rescale_q(pkt.dts, avctx->time_base, out_stream->time_base);
        pkt.dts = pkt.pts; //++Huey
        pkt.duration = av_rescale_q(pkt.duration, avctx->time_base, out_stream->time_base);


        ret = av_interleaved_write_frame(ofmt_ctx, &pkt);
        //ret = av_write_frame(ofmt_ctx, &pkt);    //++Huey

        // qDebug() << "end --------------------" << ret;
    }

    return 0;
}