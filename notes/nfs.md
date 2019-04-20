### 关于NFS前置使用http并发请求会报错NoHttpResponseException异常分析
- 在此可以了解一下http Connection Keep-Alive <https://www.cnblogs.com/web21/p/6397525.html>
- http客户端采用org.apache.http.impl.client.CloseableHttpClient，此客户端源代码会复用http连接
`  
  public final ConnectionRequest requestConnection(final HttpRoute route, final Object state) {
         Args.notNull(route, "Route");
         return new ConnectionRequest() {
             public boolean cancel() {
                 return false;
             }
 
             public HttpClientConnection get(long timeout, TimeUnit tunit) {
                 return BasicHttpClientConnectionManager.this.getConnection(route, state);
             }
         };
     }
`

- 服务端实现http服务器采用netty实现，实现内容大体如下

```$xslt
			serverBootstrap = new ServerBootstrap();
			serverBootstrap.group(bossGroup, workerGroup).channel(NioServerSocketChannel.class)
					.option(ChannelOption.SO_BACKLOG, backlog).childHandler(new ChannelInitializer<SocketChannel>() {

						@Override
						protected void initChannel(SocketChannel ch) throws Exception {
							// 清除线程变量
							KC.threadLocal.clear();
							if (sslHandler != null) {
								ch.pipeline().addLast(sslHandler);
							}
							ch.pipeline().addLast(new HttpRequestDecoder());
							ch.pipeline().addLast(new HttpObjectAggregator(Integer.MAX_VALUE));
							ch.pipeline().addLast(new HttpResponseEncoder());
							ch.pipeline().addLast(new ChunkedWriteHandler());
							ch.pipeline().addLast(serviceHandler);
						}
					});
		}
		
		//serverhandler 的部分实现如下：
                ByteBuf contentBuf = Unpooled.copiedBuffer(contentStr, CharsetUtil.UTF_8);
                FullHttpResponse response = new DefaultFullHttpResponse(HTTP_1_1, BAD_REQUEST, contentBuf);
                response.headers().set(Names.CONTENT_TYPE, new MimeType("application", "json", Charset.forName("utf-8")));
                response.headers().set(Names.CONTENT_LENGTH, contentBuf.readableBytes());
                ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE);

```

- 通过WireShark抓包分析发现，不管header Connection 设置为close或者alive,因为服务实现不管connection如何设置
都会close这次的tcp请求。主动断开的一方总是服务器（这里抓包细节没有展示），由于在并发过程中，
客户端可能复用了上次的tcp连接，当服务器处理完此连接上次的请求后就是主导断开连接发送FIN包，当第二个http客户端处理读操作时
发现收到了FIN包，或者发送请求时，服务器发现此连接处理time_wait_1,或者time_wait状态，会直接向客户端回复RST包，导致客户端
抛出NoHttpResponseException异常。关于time_wait状态可以参考 <https://www.cnblogs.com/softidea/p/5741192.html>,
如果服务器一直处于主动断开连接的一方，将会出现大量的time_wait的socket文件句柄

- 处理方式，目前已经更改http客户端，并使用连接池方式，并改用org.apache.commons.httpclient 工具类。此方式可以不用更改
服务端能解决NoHttpResponseException 的问题


```$xslt
    /**
     * 创建客户端连接池
     */
    private void createConnectionPool() {
        if (connectionManager == null) {
            synchronized (this) {
                if (connectionManager == null) {
                    // 创建一个线程安全的HTTP连接池
                    connectionManager = new MultiThreadedHttpConnectionManager()
                    HttpConnectionManagerParams params = new HttpConnectionManagerParams()
                    // 建立连接请求的超时时间
                    params.setConnectionTimeout(connectionTimeout)
                    // 数据请求等待返回超时时间
                    params.setSoTimeout(waitTimeout)
                    // 客户端请求连接池连接单个主机的保持连接数
                    params.setDefaultMaxConnectionsPerHost(maxConnectionsPerHost)
                    // 客户端请求连接池连接所有主机总保持连接数
                    params.setMaxTotalConnections(maxTotalConnections)
                    connectionManager.setParams(params)
                }
            }
        }
    }

``` 

- 更改服务器主动断开连接逻辑

改前

```$xslt
ctx.writeAndFlush(response).addListener(ChannelFutureListener.CLOSE)
```

改后

```$xslt
    ChannelFuture feature = ctx.writeAndFlush(response);
    //TODO: 下面需不需要这样主动断开连接还需要收集一些资料确定一下
    //if (!keep-alive) {
    //   feature.addListener(ChannelFutureListener.CLOSE);
    //}

```

- 服务器这样更改只是一个建议写法，这样更改后，在不更改客户端的逻辑，并行执行40*20（启动40个线程，每个线程20次），没有一次错误
改之前一般执行3*1就会出现此种问题



