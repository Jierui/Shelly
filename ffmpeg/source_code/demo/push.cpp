extern "C" {
#include<libavformat/avformat.h>
#include<libavutil/time.h>
#include<stdio.h>
}
#include<iostream>
using namespace std;

static double r2d(AVRational r)
{
	return r.num == 0 || r.den == 0 ? 0. : (double)r.num / (double)r.den;
}



int main(int argc, char* argv[]) {
    if (argc < 3) {
        return -1;
    }
    //注册所有封装器
    av_register_all();

    //注册所有网络协议
    avformat_network_init();

    AVFormatContext* input_ctx = NULL;
    AVFormatContext* out_ctx = NULL;
    // AVInputFormat;
    int ret = 0;
    ret = avformat_open_input(&input_ctx, argv[1],NULL, NULL);
    printf("avformat_open_input ret:%d\n", ret);
    if (ret < 0 ) {
        return -1;
    }
    ret = avformat_find_stream_info(input_ctx, NULL);
    printf("avformat_find_stream_info ret:%d\n", ret);
    if (ret != 0) {
        return -1;
    }
    av_dump_format(input_ctx, 0, argv[1], 0);

    ret = avformat_alloc_output_context2(&out_ctx, NULL, "flv", argv[2]);
    printf("avformat_alloc_output_context2 ret:%d\n", ret);
    if (ret < 0) {
        return ret;
    }
    printf("nb_streams:%d\n", input_ctx->nb_streams);

    for (int i=0;i<input_ctx->nb_streams;i++) {
        AVCodec* codec = avcodec_find_decoder(input_ctx->streams[i]->codecpar->codec_id);
        AVStream *out = avformat_new_stream(out_ctx, codec);
        if (!out) {
            printf("out stream is NULL\n");
            return -2;
        }
        avcodec_parameters_copy(out->codecpar, input_ctx->streams[i]->codecpar);
    }
    av_dump_format(out_ctx, 0, argv[2], 1);

    ret = avio_open(&out_ctx->pb, argv[2], AVIO_FLAG_READ_WRITE);
    printf("avio_open ret:%d\n", ret);
    if (ret < 0) {
        return -3;
    }

    ret = avformat_write_header(out_ctx, NULL);
    printf("avformat_write_header ret:%d\n", ret);
    if (ret < 0) {
        return -2;
    }
    AVPacket pkt;
    av_init_packet(&pkt);
    long long start_time = av_gettime();
    for(;;) {
        ret = av_read_frame(input_ctx, &pkt);
        if (ret < 0) {
            goto clean;
        }
        AVRational itime = input_ctx->streams[pkt.stream_index]->time_base;
        AVRational otime = out_ctx->streams[pkt.stream_index]->time_base;

		pkt.pts = av_rescale_q_rnd(pkt.pts, itime, otime, (AVRounding)(AV_ROUND_NEAR_INF | AV_ROUND_NEAR_INF));
		pkt.dts = av_rescale_q_rnd(pkt.pts, itime, otime, (AVRounding)(AV_ROUND_NEAR_INF | AV_ROUND_NEAR_INF));
		pkt.duration = av_rescale_q_rnd(pkt.duration, itime, otime, (AVRounding)(AV_ROUND_NEAR_INF | AV_ROUND_NEAR_INF));
        pkt.pos = -1;

		//视频帧推送速度
		if (input_ctx->streams[pkt.stream_index]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO)
		{
			AVRational tb = input_ctx->streams[pkt.stream_index]->time_base;
			//已经过去的时间
			long long now = av_gettime() - start_time;
			long long dts = 0;
			dts = pkt.dts * (1000 * 1000 * r2d(tb));
			if (dts > now)
				av_usleep(dts - now);
		}
 
		ret = av_interleaved_write_frame(out_ctx, &pkt);
		if (ret < 0)
		{
			// return XError(re);
            printf("av_interleaved_write_frame ret:%d\n", ret);
            goto clean;
        }
        av_packet_unref(&pkt);


    }

clean:
    avformat_close_input(&input_ctx);
    avio_close(out_ctx->pb);
    avformat_free_context(out_ctx);
    return 0;
}